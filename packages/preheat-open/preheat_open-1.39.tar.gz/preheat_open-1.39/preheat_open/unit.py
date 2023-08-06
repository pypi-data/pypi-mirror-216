"""
Module defining units and their auxiliary functions
"""

from datetime import datetime
from enum import Enum
from typing import Optional, Union

import pandas as pd

from .api import TIMEZONE
from .backwards_compatibility import load_parameter_old_naming, warn_deprecation_pending
from .component import Component
from .data import load_box_data, load_model_data
from .exceptions import NotFoundError
from .helpers import (
    list_to_string,
    now,
    sanitise_datetime_input,
    time_resolution_aliases,
    timedelta,
    utc,
)
from .logging import Logging
from .types import TYPE_DATETIME_INPUT


class DataAlreadyPresentInUnitWarning(RuntimeWarning):
    pass


def populate_units(*args, **kwargs):
    """DEPRECATED method"""
    warn_deprecation_pending("This method is deprecated (and not doing anything)")


class Unit(object):
    """Defines a unit in the PreHEAT sense"""

    def __init__(self, unit_type: str, unit_data: dict, load_data_by: str = "id"):
        # Type
        self.unit_type: str = unit_type
        self.unit_subtype: Optional[str] = unit_data.pop("type", None)

        # Identifier of the unit
        self.id = unit_data.pop("id", None)
        # Name of the unit
        self.name: str = unit_data.pop("name", f"{self.unit_type}_{self.id}")
        if not self.name:
            # If the name does not exist, create one out of the ID and the unit type
            self.name = f"{self.unit_type}_{self.id}"

        # list of components in the unit (PreHEAT_API.Component)
        self.components: list[Component] = self.__populate_components(unit_data)

        # Time series cache
        self.data: pd.DataFrame = pd.DataFrame()

        # State cache
        self._state: pd.DataFrame = pd.DataFrame()

        # Choose how to load the data
        self.__loads_data_by = load_data_by

    def __repr__(self) -> str:
        """String representation of the unit"""
        return f"{self.unit_type}({self.name})"

    def __populate_components(self, unit_data: dict) -> list[Component]:
        components = []
        try:
            keys_to_extract = []
            for key, value in unit_data.items():
                # Component properties: a dict w. key 'cid'
                if isinstance(value, dict) and "cid" in value:
                    keys_to_extract.append(key)
            for key in keys_to_extract:
                comp = unit_data.pop(key)
                # Let 'name' be PreHEAT name, and tag be BACNET/source name
                comp["tag"] = comp["name"]
                comp["name"] = key
                # Add PreHEAT name as description
                components.append(Component(comp))

        except TypeError:
            pass

        return components

    def load_data(
        self,
        start: TYPE_DATETIME_INPUT,
        end: TYPE_DATETIME_INPUT,
        resolution: Union[str, Enum] = "minute",
        components: Union[list[str], None] = None,
        **kwargs,
    ) -> None:
        """
        Loads data in the unit

        :param start: start of the period to load data for
        :param end: end of the period to load data for
        :param resolution: resolution to load data with (raw, 5min, minute, hour, day, week, month, year)
        :param components: components to restrict the loading to (None: no restriction)
        :param kwargs: /
        :return: /
        """
        start, end, resolution = load_parameter_old_naming(
            start, end, resolution, **kwargs
        )
        self._warn_if_data_is_loaded()
        if self.__loads_data_by == "id":
            self.data = load_model_data(
                self.get_all_component_ids(components=components),
                start,
                end,
                resolution,
            )
        elif self.__loads_data_by == "cid":
            self.data = load_box_data(
                self.get_all_component_cids(components=components),
                start,
                end,
                resolution,
            )
        else:
            raise ValueError("")
        self._ensure_continuity_of_data(resolution)

    def _ensure_continuity_of_data(self, resolution: str) -> None:
        if self.data.empty or (resolution == "raw"):
            return

        time_alias = time_resolution_aliases(resolution)

        if resolution in ["day", "week", "month", "year"]:
            # Reindexing to local time prior to frequency conversion
            self.data.index = self.data.index.tz_convert(TIMEZONE)
            self.data = self.data.asfreq(freq=time_alias)
            self.data.index = self.data.index.tz_convert(utc)
        else:
            self.data = self.data.asfreq(freq=time_alias)

    def _warn_if_data_is_loaded(self):
        if self.data.empty is False:
            Logging().warning(
                DataAlreadyPresentInUnitWarning(
                    f"Data was already present in unit (id={self.id}, name={self.name}, type={self.unit_type})"
                )
            )

    def clear_data(self, **kwargs) -> None:
        """
        Clears data from the unit

        :param kwargs: /
        :return: /
        """
        self.data = self.data[0:0]

    def cquery(self, name: str) -> Component:
        return [component for component in self.components if component.name == name][0]

    def _select_components(self, components: Union[list, None] = None) -> list:
        if components is None:
            return self.components
        else:
            if isinstance(components, str):
                components = [components]
            return [
                component
                for component in self.components
                if component.name in components
            ]

    def get_all_component_cids(
        self, prefix: bool = False, components: Union[list, None] = None
    ):
        prefix = "{}.".format(self.name) if prefix else ""
        comps = self._select_components(components=components)
        return {str(c.cid): prefix + c.name for c in comps}

    def get_all_component_ids(
        self, prefix: bool = False, components: Union[list, None] = None
    ) -> dict[str, str]:
        prefix = "{}.".format(self.name) if prefix else ""
        comps = self._select_components(components=components)
        return {str(c.id): prefix + c.name for c in comps}

    def get_all_component_details(
        self, prefix: bool = False, components: Union[list, None] = None
    ) -> list[dict[str, Union[str, float, None]]]:
        prefix = f"{self.name}." if prefix else ""
        comps = self._select_components(components=components)

        return [
            {
                "id": str(c.id),
                "cid": str(c.cid),
                "name": prefix + c.name,
                "stdUnitDivisor": c.std_unit_divisor,
                "stdUnitDevisor": c.std_unit_divisor,  # Kept for backwards compatibility (despite typo)
                "stdUnit": c.std_unit,
            }
            for c in comps
        ]

    def get_component(self, name: str) -> Component:
        """
        Returns the component with the given name

        :param name: name of the component to look for
        :raise: NotFoundError if no component with the given name is found
        :return: component with the chosen name
        """
        try:
            return [
                component for component in self.components if component.name == name
            ][0]
        except Exception as e:
            raise NotFoundError(
                f"The component ({name}) does not exist in the unit ({self.name})."
            ) from e

    def has_component(self, component_name: str) -> bool:
        """
        Tells if a unit a given component

        :param component_name: name of the component to look for
        :return: True if the unit has a component with the given name, False otherwise
        """
        try:
            c = self.get_component(component_name)
            out = isinstance(c, Component)
        except NotFoundError as e:
            out = False
        return out

    def has_data(
        self,
        component: Union[str, None] = None,
        check_not_null: bool = True,
    ) -> bool:
        """
        Tells whether the unit has data

        :param component: if non-None, tells whether data is available for the specific component
        :param check_not_null: if True, checks that the data is not null
        :return: True if data is available, False otherwise
        """
        if component is None:
            return len(self.data) > 0
        elif self.has_component(component) is False:
            return False
        elif self.data.empty is True:
            return False
        elif component in self.data.columns and self.data.shape[0] > 0:
            return self.data[component].notnull().any() if check_not_null else True
        else:
            return False

    # Methods to manage unit state
    def load_state(
        self,
        seconds_back: int = 300,
        t_now: Union[datetime, None] = None,
        resolution_overwrite: Optional[str] = None,
    ) -> None:
        """
        Loads the state of the unit at a given point in time

        :param seconds_back: number of seconds back prior to t_now to look for data for
            (if none is found in the interval, then value will be NaN for this component)
        :param t_now: now-time override
        :param resolution_overwrite: if specified, then loads the data using that specific resolution
            (by default, data is loaded in "raw" resolution if t_now is more recent than 7 days ago, else "5min")
        :return: /
        """
        t_now = now() if t_now is None else sanitise_datetime_input(t_now)
        # Check if recent enough to expect raw data
        if resolution_overwrite is not None:
            resolution = resolution_overwrite
        elif t_now > now() - timedelta(days=7):
            resolution = "raw"
        else:
            resolution = "minute"
        self._state = load_model_data(
            self.get_all_component_ids(),
            t_now - timedelta(seconds=seconds_back),
            t_now,
            resolution,
        )

    def clear_state(self, **kwargs) -> None:
        """
        Clears the state data from the unit

        :param kwargs: /
        :return: /
        """
        self._state = pd.DataFrame()

    def get_state(
        self,
        update: bool = False,
        estimate: str = "last",
        seconds_back: int = 300,
        t_now: Union[datetime, None] = None,
        by: str = "id",
        resolution_overwrite: Optional[str] = None,
    ) -> pd.Series:
        """
        Fetches the state for the given unit (to force refresh it, update is required)

        :param update: if True, loads the state data to update it, else just fetches the state already loaded
        :param estimate: method to use for state estimation
            ("last" for last available value, "mean" for average in period, "median" for median value in period)
        :param seconds_back: number of seconds before t_now to look for when loading data
        :param t_now: now-time override
        :param by: whether to load data by "id" or component id "cid"
        :param resolution_overwrite: if specified, then loads the data using that specific resolution
            (by default, data is loaded in "raw" resolution if t_now is more recent than 7 days ago, else "5min")
        :return: unit state in pandas Series format
        """
        if update is True:
            self.load_state(
                seconds_back=seconds_back,
                t_now=t_now,
                resolution_overwrite=resolution_overwrite,
            )

        if (self._state is None) or self._state.empty:
            if by == "id":
                state = pd.Series(
                    index=self.get_all_component_ids().values(), dtype=float
                )
            elif by == "cid":
                state = pd.Series(
                    index=self.get_all_component_cids().values(), dtype=float
                )
            else:
                raise ValueError(
                    f"Bad value for 'by' input ({by}) must be either id or cid"
                )
        elif estimate == "last":
            state = self._state.ffill().iloc[-1, :]
        elif estimate == "mean":
            state = self._state.mean()
        elif estimate == "median":
            state = self._state.median()
        else:
            raise Exception(f"Invalid value for estimate ({estimate})")

        return state

    def describe(
        self,
        display: bool = True,
        prefix: str = "",
        components: bool = True,
        show_subtype: bool = True,
        **kwargs,
    ) -> str:
        """
        Generate a text-based description of a unit

        :param display: if True, prints the output
        :param prefix: string prefix to each output line (use for tabs, etc)
        :param components: if True, outputs components details
        :param show_subtype: if True, shows the sub-type of units
        :param kwargs: /
        :return: text description of units as string
        """
        if show_subtype:
            subtype = f" / sub-type={self.unit_subtype}"
        else:
            subtype = ""
        out = prefix + f"[{self.unit_type}] {self.name} [id={self.id}{subtype}]"
        if components:
            out += ": " + list_to_string([c.name for c in self.components])
        if display:
            print(out)
        return out
