"""
Module defining building units and their auxiliary methods
"""
from __future__ import annotations

import re
from enum import Enum
from typing import Optional, Union

from .backwards_compatibility import load_parameter_old_naming
from .helpers import (
    check_no_remaining_fields,
    convenience_result_list_shortener,
    sanitise_unit_type_input,
)
from .logging import Logging
from .types import TYPE_DATETIME_INPUT
from .unit import Unit
from .weather import Weather


def populate_units(unit_type, units_data, building_ref):
    # Loop over units; create and populate Unit instances
    units = [BuildingUnit(unit_type, unit_i, building_ref) for unit_i in units_data]
    return units


def add_unique_units(units, new_units, ids) -> None:
    for item in new_units:
        if item.id not in ids:
            units.append(item)
            ids.append(item.id)


def exclude_shared_units_from_list(x: list[BaseBuildingUnit]) -> list[BaseBuildingUnit]:
    return [u for u in x if not u.is_shared()]


class BaseBuildingUnit(Unit):
    """Building Unit; an extension of Unit to handle zones and parent units"""

    def __init__(
        self,
        unit_type: str,
        unit_data: dict[str, Union[str, float, bool, None]],
        building_ref,
        load_data_by: str = "id",
    ):
        super().__init__(unit_type, unit_data, load_data_by=load_data_by)

        # Building reference
        self.building = building_ref

        # Zones covered (Attempt to first extract 'zoneIds', then ['zoneId']), and couple zones
        self.zone_ids = []
        self.__zones = []
        zone_ids = unit_data.pop("zoneIds", None)
        if zone_ids is None:
            if "zoneId" in unit_data:
                zone_ids = [unit_data.pop("zoneId", None)]
            else:
                zone_ids = []
        [self.__add_zone(zone_id) for zone_id in zone_ids]
        [z_i.add_coupled_unit(self) for z_i in self.__zones]

        # Indication on whether the unit is shared
        self.__shared = ("shared" in unit_data) and unit_data.pop("shared")

    def __add_zone(self, zone_id):
        self.zone_ids.append(zone_id)
        self.__zones += self.building.get_zones([zone_id])

    def parents(self) -> list[BaseBuildingUnit]:
        return [
            self.building.unit_graph.nodes[item[0]]["unit"]
            for item in self.building.unit_graph.pred[self.id].items()
        ]

    @property
    def weather(self) -> Weather:
        return self.building.weather

    # Taken from open API: building_unit.py
    def query_parent_units(
        self,
        unit_type: Optional[str] = None,
        name: Optional[str] = None,
        exclude_shared: bool = False,
        _depth: int = 5,
    ) -> list[BaseBuildingUnit]:
        # if no levels left to traverse no parents to output
        if _depth < 1 or type(_depth) is not int:
            return []
        # If we pass a unit_type, check if we do regex search or strict search
        if unit_type:
            if unit_type[0] == "?":
                r_type = re.compile(unit_type[1:])
                type_match = lambda t: r_type.search(t)
            else:
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
                    unit
                    for unit in self.parents()
                    if name_match(unit.name) and type_match(unit.unit_type)
                ]

            elif name:
                result = [unit for unit in self.parents() if name_match(unit.name)]

            elif unit_type:
                result = [unit for unit in self.parents() if type_match(unit.unit_type)]

        except Exception as e:
            Logging().warning(f"Error when querying parent units ({str(e)})")
            result = []

        # add one step up
        if _depth > 1:
            res_id = [p.id for p in result]
            new_depth = _depth - 1
            for parent in self.parents():
                if type(parent) is BuildingUnit:
                    next = parent.query_parent_units(
                        unit_type=unit_type, name=name, _depth=new_depth
                    )
                    add_unique_units(result, next, res_id)

        if exclude_shared:
            result = exclude_shared_units_from_list(result)

        return result

    def qpu(self, *args, **kwargs) -> Union[BaseBuildingUnit, list[BaseBuildingUnit]]:
        result = self.query_parent_units(*args, **kwargs)
        return convenience_result_list_shortener(result)

    def get_zones(self):
        return self.__zones

    def query_units(self, *args, **kwargs) -> list[BaseBuildingUnit]:
        return []

    def qu(self, *args, **kwargs) -> Union[BaseBuildingUnit, list[BaseBuildingUnit]]:
        result = self.query_units(*args, **kwargs)
        return convenience_result_list_shortener(result)

    # Experimental functions below, use with care
    def is_shared(self) -> bool:
        return self.__shared


class BuildingUnit(BaseBuildingUnit):
    """Building Unit; an extension of BaseBuildingUnit to handle subUnits"""

    def __init__(self, unit_type, unit_data, building_ref):
        from .control_unit import ControlUnit

        super().__init__(unit_type, unit_data, building_ref)

        # Sub-units (preheat_open.BuildingUnit list)
        self.sub_units = []
        self.__sub_unit_ids = []
        unit_types = [
            "subVentilations",
            "secondaries",
            "subHeating",
            "heatingCoils",
            "coolingCoils",
            "heatRecovery",
            "secondaryCirculation",
            "secondaryTank",
            "secondaryHeatExchanger",
            "secondaryHeatExchangerWithTank",
            "subMeters",
            "radiators",
            "floorHeatingLoops",
        ]

        [
            self.add_sub_unit(
                populate_units(unit_type, unit_data.pop(unit_type, []), building_ref)
            )
            for unit_type in unit_types
        ]

        # Controls
        _controls = unit_data.pop("controls", [])
        [self.add_sub_unit(ControlUnit(control, building_ref)) for control in _controls]

        # These units and maters need to be linked at a later stage when available in the building
        self._related_sub_units_refs = []
        self._related_sub_units_refs += unit_data.pop("heatingCoilIds", [])
        self._related_sub_units_refs += unit_data.pop("coolingCoilIds", [])
        # self.sub_unit_refs += unit_data.pop("zoneIds", [unit_data.pop("zoneId", [])])
        self._related_meters_refs = []
        meter_labels = [
            "electricityId",
            "mainId",
            "heatingId",
            "hotWaterId",
            "coldWaterId",
        ]
        for label in meter_labels:
            if label in unit_data and unit_data[label]:
                self._related_meters_refs.append(unit_data.pop(label))

        # For now, this is a protected attribute
        self._meters = []

        check_no_remaining_fields(unit_data, debug_helper="building_unit_data")

    def add_sub_unit(self, u):
        if isinstance(u, list):
            [self.add_sub_unit(u_i) for u_i in u]
        elif isinstance(u, Unit):
            if u.id not in self.__sub_unit_ids:
                self.sub_units += [u]
                self.__sub_unit_ids += [u.id]
        else:
            TypeError(f"Invalid type for input u ({type(u)}")

    def load_data(
        self,
        start: TYPE_DATETIME_INPUT,
        end: TYPE_DATETIME_INPUT,
        resolution: Union[str, Enum] = "minute",
        load_children=False,
        components=None,
        **kwargs,
    ) -> None:
        start, end, resolution = load_parameter_old_naming(
            start, end, resolution, **kwargs
        )
        super().load_data(start, end, resolution=resolution, components=components)
        if load_children is True:
            [
                u_i.load_data(
                    start,
                    end,
                    resolution=resolution,
                    load_children=True,
                )
                for u_i in self.children()
            ]

    def clear_data(self, clear_children: bool = False) -> None:
        super().clear_data()
        if clear_children:
            [u_i.clear_data(clear_children=True) for u_i in self.children()]

    def children(self) -> list[BaseBuildingUnit]:
        return [
            self.building.unit_graph.nodes[item[0]]["unit"]
            for item in self.building.unit_graph.succ[self.id].items()
        ]

    def query_units(
        self,
        unit_type: Optional[str] = None,
        name: Optional[str] = None,
        exclude_shared: bool = False,
        _depth: int = 10,
    ) -> list[BaseBuildingUnit]:
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
            # Now ensuring that all children units are queried through (not only sub-units)
            candidate_units = self.children()
            children_units_id = [u.id for u in candidate_units]
            for u in self.sub_units + self._meters:
                if u.id not in children_units_id:
                    children_units_id += [u.id]
                    candidate_units += [u]

            # If we pass unit_type and name
            if unit_type and name:
                result = [
                    unit
                    for unit in candidate_units
                    if name_match(unit.name) and type_match(unit.unit_type)
                ]

            elif name:
                result = [unit for unit in candidate_units if name_match(unit.name)]

            elif unit_type:
                result = [
                    unit for unit in candidate_units if type_match(unit.unit_type)
                ]

            # Querying also through children units
            for u_i in candidate_units:
                next_depth = _depth - 1
                result += u_i.query_units(
                    unit_type=unit_type, name=name, _depth=next_depth
                )

            if exclude_shared:
                result = exclude_shared_units_from_list(result)

            return result

        except Exception as e:
            Logging().warning(f"Error when querying parent units ({str(e)})")
            return []

    def describe(
        self, display: bool = True, prefix: str = "", children: bool = True, **kwargs
    ) -> str:
        out = super().describe(display=display, prefix=prefix, **kwargs)
        unit_children = self.children()
        if children is False or len(unit_children) == 0:
            pass  # out += "\n"
        else:
            for u in unit_children:
                out += "\n" + u.describe(
                    display=False, prefix=prefix.replace("-", "") + "\t- ", **kwargs
                )
        if display:
            print(out)
        return out
