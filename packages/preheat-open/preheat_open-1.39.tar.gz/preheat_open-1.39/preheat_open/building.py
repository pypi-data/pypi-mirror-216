"""
Module defining the Building class, which represents buildings containing different units and their data
"""
import re
from enum import Enum
from typing import Any, Optional, Union

import networkx as nx
import pandas as pd

from . import unit_graph
from .api import AccessDeniedError, api_get
from .backwards_compatibility import load_parameter_old_naming, warn_deprecation_pending
from .building_unit import (
    BaseBuildingUnit,
    exclude_shared_units_from_list,
    populate_units,
)
from .comfort_profiles import fetch_comfort_profiles
from .data import load_model_data
from .device import Device
from .exceptions import NoComfortProfileError
from .helpers import (
    check_no_remaining_fields,
    convenience_result_list_shortener,
    sanitise_datetime_input,
    sanitise_unit_type_input,
)
from .price import SupplyPoint
from .types import TYPE_DATETIME_INPUT
from .unit import Unit
from .weather import Weather
from .zone import Zone, populate_zones, zone_matches

# When adding new unit hierarchies, these need to be added explicitly in the list
# WARNING: Order is important due to cross-dependency
_TOP_LEVEL_UNIT_TYPES = [
    "main",
    "coldWater",
    "heating",
    "hotWater",
    "cooling",
    "electricity",
    "ventilation",
    "heatPumps",
    "indoorClimate",
    "custom",
    "localWeatherStations",
    "pvs",
    "carChargers",
]


class Building(object):
    """Building defines a building in the PreHEAT sense"""

    def __init__(self, location_id: int):
        self.location_id = location_id

        # dict containing the details of the location
        self.location: dict[str, Any] = {}
        # list of zones within the building (of class PreHEAT_API.Zone)
        self.zones: list[Zone] = []
        # dict w.units within the building (of class PreHEAT_API.Unit)
        self.units = {}
        # dict w. weather information for the location (PreHEAT_API.Weather)
        self.weather = None  # type: Weather
        # Area of the building
        self.area = None
        # All characteristics get summarised in this dictionary
        # (duplicate with some attributes do to backwards-compatibility requirement)
        self.characteristics = {}

        # Supply points (for pricing)
        self.__supply_points = []

        # Load from API
        self.__populate()

        # Construct graph
        self.__unit_graph = unit_graph.generate_unit_graph(self)

        # Traverse and map sub-unit references
        for u in self.iterate_units():
            # Add sub-units as new nodes
            if hasattr(u, "_related_sub_units_refs"):
                for ref in u._related_sub_units_refs:
                    u.add_sub_unit(self.unit_graph.nodes[ref]["unit"])
            if hasattr(u, "_related_meters_refs"):
                for ref in u._related_meters_refs:
                    u._meters.append(self.unit_graph.nodes[ref]["unit"])

        # Devices
        self.__devices: Optional[list[Device]] = None

        # Comfort profiles
        self.__comfort_profile_data = None

    def iterate_units(self) -> list[BaseBuildingUnit]:
        out = [data["unit"] for node, data in self.unit_graph.nodes.data()]
        return out

    @property
    def unit_graph(self) -> nx.MultiDiGraph:
        return self.__unit_graph

    @property
    def G(self) -> nx.MultiDiGraph:
        """DEPRECATED: use the 'unit_graph' attribute instead"""
        warn_deprecation_pending(
            "The 'G' attribute is deprecated - use the 'unit_graph' attribute instead"
        )
        return self.unit_graph

    def get_unit_graph(self) -> nx.MultiDiGraph:
        """DEPRECATED: use the 'unit_graph' attribute instead"""
        warn_deprecation_pending(
            "The 'get_unit_graph' method is deprecated - use the 'unit_graph' attribute instead"
        )
        return self.unit_graph

    def load_comfort_profile_data(
        self, start: TYPE_DATETIME_INPUT, end: TYPE_DATETIME_INPUT
    ) -> None:
        """
        Loads the comfort profile data in the building object

        :param start: start of the period
        :param end: end of the period
        """
        try:
            self.__comfort_profile_data = fetch_comfort_profiles(
                self.location_id, start=start, end=end
            )
        except NoComfortProfileError:
            pass

    def clear_comfort_profile_data(self):
        """
        Clears the comfort profile data loaded in the building object
        """
        self.__comfort_profile_data = None

    @property
    def comfort_profile_data(self) -> pd.DataFrame:
        """
        Convenience accessor to the comfort profile data for the building, if only one is defined.

        :raise: NoComfortProfileError if no data is loaded/available or if there are too many comfort profiles
            for the building
        """
        return self.get_comfort_profile_data(None)

    def get_comfort_profile_data(
        self, comfort_profile_id: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Accessor to the comfort profile data for a given comfort_profile_id.
        This requires prior loading via the *load_comfort_profile_data* method.

        :param comfort_profile_id: ID of the comfort profile, if None tries to access the only comfort profile in
            the building (for convenience in small buildings without zones) and fails if too many available
        :raise: NoComfortProfileError if no data is loaded or available
        :return: dictionary of comfort profiles (key=comfort profile ID, value=dataframe[setpoint, min, max, value])
        """
        if self.__comfort_profile_data is None:
            raise NoComfortProfileError("No comfort profile loaded/available")
        elif comfort_profile_id is None:
            if len(self.__comfort_profile_data) == 1:
                out = list(self.__comfort_profile_data.values())[0]
            else:
                raise ValueError(
                    "Too many comfort profiles available (the shortcut only works when only one is available)"
                )
        else:
            out = self.__comfort_profile_data.get(comfort_profile_id)
            if out is None:
                raise NoComfortProfileError(
                    "No comfort profile available for the comfort_profile_id"
                )

        return out

    def load_data(
        self,
        start: TYPE_DATETIME_INPUT,
        end: TYPE_DATETIME_INPUT,
        resolution: Union[str, Enum] = "hour",
        components: Optional[dict[str, list[str]]] = None,
        **kwargs,
    ) -> None:
        """
        Loads timeseries data in the units of a building

        :param start: start time of the data loading
        :param end: end time of the loading
        :param resolution: resolution of the data to be loaded
        :param components: mapping of the data to be loaded (None to load everything), where the key is the unit type,
            and the value is a list of the components to load (None to load them all)
        :return: /
        """

        if components is None:
            components = {}

        start, end, resolution = load_parameter_old_naming(
            start, end, resolution, **kwargs
        )

        start = sanitise_datetime_input(start)
        end = sanitise_datetime_input(end)
        if components is None:
            components = {}

        if len(components) == 0:
            # Load all data on building, if nothing is specified
            for u in self.list_all_units():
                c_i = components.get(u.unit_type)
                u.load_data(start, end, resolution, components=c_i)
        else:
            # Otherwise, just load specific components
            for i in components.keys():
                c_i = components.get(i)
                if i == "weather":
                    self.weather.load_data(start, end, resolution, components=c_i)
                else:
                    [
                        u_i.load_data(start, end, resolution, components=c_i)
                        for u_i in self.query_units(unit_type=i)
                    ]

    def list_all_units(self) -> list[Unit]:
        out = [self.weather] + self.iterate_units()
        return out

    def load_dataset(
        self,
        component_map,
        start: TYPE_DATETIME_INPUT,
        end: TYPE_DATETIME_INPUT,
        resolution: str = "hour",
        load_weather: bool = True,
    ) -> pd.DataFrame:
        """

        :param component_map:
        :param start:
        :param end:
        :param resolution:
        :param load_weather:
        :return:
        """

        df = load_model_data(component_map, start, end, resolution)

        if load_weather is True:
            self.weather.load_data(start, end, resolution)
            df_weather = self.weather.data
            df_weather.columns = "weather." + df_weather.columns
            df = pd.concat((df_weather, df), axis=1)

        return df

    def clear_data(self) -> None:
        """
        Clears all data in the units of the object

        :return: /
        """
        self.weather.clear_data()
        [u.clear_data() for u in self.iterate_units()]

    def get_all_component_ids(self) -> dict:
        """

        :return:
        """
        return {
            k: v
            for u in self.iterate_units()
            for k, v in u.get_all_component_ids(True).items()
        }

    def get_all_component_details(self) -> list[dict[str, Union[str, float, None]]]:
        """

        :return:
        """
        all_comps = []
        for u in self.iterate_units():
            all_comps += u.get_all_component_details(prefix=True)

        return all_comps

    def query_units(
        self,
        unit_type: str = None,
        name: str = None,
        unit_id: int = None,
        exclude_shared: bool = False,
    ) -> list[BaseBuildingUnit]:
        """

        :param unit_type:
        :param name:
        :param unit_id:
        :param exclude_shared: if True, excludes shared units
        :return: a list of the relevant units
        """
        # If we pass a unit ID, find specific unit
        if unit_id:
            if unit_id in self.unit_graph.nodes.keys():
                out = [self.unit_graph.nodes[unit_id]["unit"]]
            else:
                out = []

        else:
            # If we pass a unit_type, check if we do regex search or strict search
            if unit_type:
                if unit_type[0] == "?":
                    r_type = re.compile(unit_type[1:])
                    type_match = lambda t: r_type.search(t)
                else:
                    unit_type = sanitise_unit_type_input(unit_type)
                    type_match = lambda t: t == unit_type

            # If we pass name, check if we do regex search or strict search
            if name:
                # Check if we do strict search or search by regex:
                if name[0] == "?":
                    r_name = re.compile(name[1:])
                    name_match = lambda n: r_name.search(n)
                else:
                    name_match = lambda n: n == name

            try:
                # If we pass unit_type and name
                if unit_type and name:
                    result = [
                        u
                        for u in self.iterate_units()
                        if name_match(u.name) and type_match(u.unit_type)
                    ]

                elif name:
                    result = [u for u in self.iterate_units() if name_match(u.name)]

                elif unit_type:
                    result = [
                        u for u in self.iterate_units() if type_match(u.unit_type)
                    ]

                out = result

            except Exception:
                out = []

        if exclude_shared:
            out = exclude_shared_units_from_list(out)

        return out

    def qu(self, *args, **kwargs) -> Union[BaseBuildingUnit, list[BaseBuildingUnit]]:
        """
        Convenience version of the query_units method

        :param args:
        :param kwargs:
        :return:
        """
        result = self.query_units(*args, **kwargs)
        return convenience_result_list_shortener(result)

    def __populate(self) -> None:
        # Request PreHEAT API for location
        resp = api_get(f"locations/{self.location_id}", out="json")

        # Check if we have building data and if we do, extract and populate
        if "building" in resp:
            data = resp["building"]

            self.location = data.pop("location")
            self.area = data.pop("buildingArea")
            self.type = data.pop("buildingType")
            self.characteristics = {
                "area": self.area,
                "type": self.type,
                "apartments": data.pop("apartments"),
            }

            self.weather = Weather(self.location_id, data.pop("weatherForecast"))
            self.zones = populate_zones(data.pop("zones"), building=self)

            for unit_type in _TOP_LEVEL_UNIT_TYPES:
                self.units[unit_type] = populate_units(
                    unit_type, data.pop(unit_type), self
                )

            for sp_i in data.pop("supplyPoints"):
                self.__supply_points.append(SupplyPoint(sp_i))

        else:
            raise AccessDeniedError("Access denied for given building")

        # For development validation, validate that no fields are left
        check_no_remaining_fields(data, debug_helper="building_data[building]")

    def get_supply_points(self) -> list:
        """

        :return:
        """
        return self.__supply_points

    def __repr__(self) -> str:
        return f"""{type(self).__name__}({self.location_id}): {self.location["address"]} - {self.type}"""

    def get_zones(self, zone_ids) -> list[Zone]:
        """

        :param zone_ids:
        :return:
        """
        res = []
        for z_i in self.zones:
            if z_i.id in zone_ids:
                res.append(z_i)
            res += z_i.get_sub_zones(zone_ids=zone_ids)
        return res

    def get_zone(self, id: int) -> Zone:
        """

        :param id:
        :return:
        """
        zs = self.get_zones([id])
        n_zs = len(zs)
        if n_zs < 1:
            raise Exception(f"Zone not found (id={id})")
        elif n_zs > 1:
            raise Exception(f"Too many zones found for id (id={id} / {n_zs} found)")
        return zs[0]

    def describe(self, display: bool = True) -> str:
        apartments = self.characteristics.get("apartments")
        out = """ID: {id}
Address: {address}
City: {city}
Country: {country}

Type: {building_type}
Heated area: {area}
{apartments}

Units:
==============================\n""".format(
            id=self.location_id,
            address=self.location.get("address"),
            city=self.location.get("city"),
            country=self.location.get("country"),
            building_type=self.characteristics.get("type"),
            area=self.characteristics.get("area"),
            apartments=(
                "Apartments: {}".format(apartments) if apartments is not None else ""
            ),
        )

        main_was_found = False

        for i in _TOP_LEVEL_UNIT_TYPES:
            units_i = self.query_units(i)
            if len(units_i) == 0:
                continue
            elif i == "main":
                main_was_found = True
            elif main_was_found and i in ["heating", "hotWater"]:
                continue  # Skip heating and hot water, as they are already listed under the main

            out += "    [{}] \n".format(i.upper())
            for u in units_i:
                out += u.describe(display=False, prefix="\t -", children=True) + "\n"
            out += "\n"

        out += """
Zones:
==========================\n"""
        zones = self.zones
        if len(zones) == 0:
            out += "(None)\n"
        else:
            for z in zones:
                out += z.describe(prefix="- ", children=True, display=False) + "\n"

        if display:
            print(out)
        return out

    # Managing devices
    def load_devices(self) -> None:
        """
        Loads the devices structure for the building (raw sensor structure)
        """
        resp = api_get(f"locations/{self.location_id}/devices", out="json")
        devices = resp["devices"]
        self.__devices = []
        for d in devices:
            d_type = d["typeName"]
            device_d = Device(d_type, d, self)
            self.__devices.append(device_d)

    def load_device_data(
        self,
        start: TYPE_DATETIME_INPUT,
        end: TYPE_DATETIME_INPUT,
        resolution: str = "hour",
    ):
        [d.load_data(start, end, resolution) for d in self.devices]

    def clear_device_data(
        self,
    ):
        [d.clear_data() for d in self.devices]

    @property
    def devices(self) -> list[Device]:
        if self.__devices is None:
            self.load_devices()
        return self.__devices

    def describe_devices(self, display: bool = True) -> str:
        apartments = self.characteristics.get("apartments")
        out = """ID: {id}
Address: {address}
City: {city}
Country: {country}

Type: {building_type}
Heated area: {area}
{apartments}

Devices:
==============================\n""".format(
            id=self.location_id,
            address=self.location.get("address"),
            city=self.location.get("city"),
            country=self.location.get("country"),
            building_type=self.characteristics.get("type"),
            area=self.characteristics.get("area"),
            apartments=(
                "Apartments: {}".format(apartments) if apartments is not None else ""
            ),
        )

        for d in self.devices:
            out += d.describe(display=False, prefix="\t -", children=False) + "\n"
        out += "\n"

        if display:
            print(out)
        return out

    def query_devices(
        self,
        name: Optional[str] = None,
        id: Optional[int] = None,
        device_type: Optional[str] = None,
    ) -> list[Device]:
        out = []
        for i in self.devices:
            add_i = None
            if name is not None:
                add_i = i.name == name
            if id is not None:
                if add_i is None:
                    add_i = True
                add_i = add_i and (i.id == id)
            if device_type is not None:
                if add_i is None:
                    add_i = True
                add_i = add_i and (i.unit_type == device_type)
            if add_i:
                out.append(i)
        return out

    def query_zones(
        self, zone_id: Optional[int] = None, zone_type: Optional[str] = None
    ) -> list[Zone]:
        out = []
        for z in self.zones:
            if zone_matches(z, zone_id=zone_id, zone_type=zone_type):
                out += [z]
            out += z.query_zones(zone_id=zone_id, zone_type=zone_type)
        return out


def available_buildings() -> pd.DataFrame:
    """
    lists available buildings

    :return: dataframe of buildings available
    :rtype:
    """
    out = api_get("locations")
    return pd.DataFrame(out["locations"])
