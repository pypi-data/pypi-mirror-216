"""
Module to manage devices
"""

from datetime import datetime
from typing import Optional, Union

import pandas as pd

from preheat_open.building_unit import BaseBuildingUnit

from .data import load_box_data
from .helpers import now, sanitise_datetime_input, timedelta


class Device(BaseBuildingUnit):
    """
    A device is a grouping of signals originating from a single physical data source (device),
    which is not linked to the building model
    """

    def __init__(self, unit_type: str, unit_data: dict, building_ref):
        unit_data_reshaped = {
            "coversBuilding": True,
            "zoneIds": [],
            "shared": False,
            "id": unit_data["id"],
            "name": unit_data["name"],
        }
        unit_data_reshaped |= {c["name"]: c for c in unit_data["components"]}

        super().__init__(
            unit_type, unit_data_reshaped, building_ref, load_data_by="cid"
        )

    def describe(
        self, display: bool = True, prefix: str = "", components: bool = True, **kwargs
    ) -> str:
        """
        Generate a text-based description of a device

        :param display: if True, prints the output
        :param prefix: string prefix to each output line (use for tabs, etc)
        :param components: if True, outputs components details
        :param kwargs: /
        :return: text description of units as string
        """
        return super().describe(
            display=display,
            prefix=prefix,
            components=components,
            show_subtype=False,
            **kwargs,
        )

    def load_state(
        self,
        seconds_back: int = 300,
        t_now=None,
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
        self._state = load_box_data(
            self.get_all_component_cids(),
            t_now - timedelta(seconds=seconds_back),
            t_now,
            resolution,
        )

    def get_state(
        self,
        update: bool = False,
        estimate: str = "last",
        seconds_back: int = 300,
        t_now: Union[datetime, None] = None,
        resolution_overwrite: Optional[str] = None,
        **kwargs,
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
        return super().get_state(
            update=update,
            estimate=estimate,
            seconds_back=seconds_back,
            t_now=t_now,
            by="cid",
            resolution_overwrite=resolution_overwrite,
        )
