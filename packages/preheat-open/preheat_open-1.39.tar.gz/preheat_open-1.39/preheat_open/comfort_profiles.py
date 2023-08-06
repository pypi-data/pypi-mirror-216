"""
Module to manage the comfort profiles
"""
import pandas as pd

from .api import api_get, datetime_to_api_string
from .exceptions import NoComfortProfileError
from .helpers import sanitise_datetime_input
from .types import TYPE_DATETIME_INPUT


def fetch_comfort_profiles(
    location_id: int,
    start: TYPE_DATETIME_INPUT,
    end: TYPE_DATETIME_INPUT,
) -> dict[int, pd.DataFrame]:
    """
    Get target temperature using API call
    """
    start = sanitise_datetime_input(start)
    end = sanitise_datetime_input(end)
    package = api_get(
        f"locations/{location_id}/comfortprofile/setpoints",
        payload={
            "start_time": datetime_to_api_string(start),
            "end_time": datetime_to_api_string(end),
        },
        out="json",
    )["comfortProfiles"]
    if not package:
        raise NoComfortProfileError(
            "No comfort profile available for location in period"
        )

    data = {}
    for comfort_profile in package:
        zdf = pd.DataFrame(comfort_profile["setpoints"]).set_index("time")
        zdf.index = pd.DatetimeIndex(zdf.index)
        zdf["name"] = comfort_profile["name"]
        comfort_profile_id = comfort_profile["id"]

        # Fixing API issue by cropping the data to the focus period
        data[comfort_profile_id] = zdf[start:end]

    return data
