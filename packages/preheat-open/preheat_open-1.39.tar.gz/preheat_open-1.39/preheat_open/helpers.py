"""
Various helper functions
"""
import os
from copy import copy
from datetime import date, datetime, timedelta, timezone, tzinfo
from enum import Enum
from functools import lru_cache
from typing import Any, Optional, Union
from warnings import warn

import dateutil.parser
from dateutil.tz import tzutc

from preheat_open import TIMEZONE

from .types import TYPE_DATETIME_INPUT

utc = timezone.utc


@lru_cache(maxsize=1)
def DISPLAY_DEVELOPER_WARNING() -> bool:
    """
    Method used for development purposes to decide whether to show warnings for development

    :return: True if developer warnings should be enabled
    """
    from preheat_open import ENV_VAR_TRACK_MISSING_DATA_FIELD, running_in_test_mode

    try:
        env_var = os.environ.get(ENV_VAR_TRACK_MISSING_DATA_FIELD)
        out = running_in_test_mode() and (env_var is not None) and (env_var == "true")
    except Exception:
        out = False
    return out


def timestep_start(step: Union[Enum, str], t: datetime) -> datetime:
    """
    Computes the start of the current timestep

    :param step: step (check conditions below)
    :param t: time for which to evaluate the step start
    :return: start time of the timestep
    """
    if isinstance(step, Enum) and isinstance(step.value, str):
        step = step.value

    if step in ["second", "1s"]:
        t_start = t.replace(microsecond=0)
    elif step == "15s":
        sec_start = int(t.second / 15) * 15
        t_start = t.replace(microsecond=0, second=sec_start)
    elif step == "30s":
        sec_start = int(t.second / 30) * 30
        t_start = t.replace(microsecond=0, second=sec_start)
    elif step in ["minute", "1min"]:
        t_start = t.replace(microsecond=0, second=0)
    elif step == "5min":
        min_start = int(t.minute / 5) * 5
        t_start = t.replace(microsecond=0, second=0, minute=min_start)
    elif step == "15min":
        min_start = int(t.minute / 15) * 15
        t_start = t.replace(microsecond=0, second=0, minute=min_start)
    elif step == "30min":
        min_start = int(t.minute / 30) * 30
        t_start = t.replace(microsecond=0, second=0, minute=min_start)
    elif step == "hour":
        t_start = t.replace(microsecond=0, second=0, minute=0)
    elif step == "day":
        t_start = t.replace(microsecond=0, second=0, minute=0, hour=0)
    elif step == "month":
        t_start = t.replace(microsecond=0, second=0, minute=0, hour=0, day=1)
    elif step == "year":
        t_start = t.replace(microsecond=0, second=0, minute=0, hour=0, day=1, month=1)
    else:
        raise Exception("Unknown step: " + step)

    return t_start


def now(
    step: Union[Enum, str, None] = None, tz: Union[tzinfo, None] = TIMEZONE
) -> datetime:
    """
    Method to determine now time (and round it to the current step start if required)

    :param step: if provided, floors the current time to the start of the step
        (if None, no manipulation of the current time is made)
    :param tz: timezone (default: local danish timezone)
    :return: datetime
    """
    t = datetime.now(tz=tz)
    if step is None:
        return t
    else:
        return timestep_start(step, t)


def __enforce_imports():
    date.today() + timedelta(days=2)


def datetime_convert(param: TYPE_DATETIME_INPUT) -> datetime:
    """
    Converts a time-related input to a valid datetime input for other methods

    :param param: input to process
    :return: datetime corresponding to the input
    """
    if isinstance(param, datetime):
        dt = param
    elif isinstance(param, str):
        dt = dateutil.parser.parse(param)
        return dt if dt.tzinfo is not None else dt.replace(tzinfo=TIMEZONE)
    else:
        raise TypeError(f"No conversion from type: {type(param)}")

    return dt if dt.tzinfo is not None else dt.astimezone(TIMEZONE)


def sanitise_datetime_input(t: TYPE_DATETIME_INPUT) -> datetime:
    if isinstance(t, str):
        out = datetime_convert(t)
    else:
        out = t
    return out.astimezone(tzutc())


def time_resolution_aliases(resolution: str) -> Optional[str]:
    """
    Converts a resolution input to the corresponding pandas alias

    :param resolution: resolution input from methods in the package
    :return: representation in pandas (str) or None if raw or not found
    """
    if resolution in ["minute", "5min"]:
        return "5T"
    elif resolution == "hour":
        return "H"
    elif resolution == "day":
        return "D"
    elif resolution == "week":
        return "7D"  # W has poor performance, as the first day of week isn't monday
    elif resolution == "month":
        return "MS"
    elif resolution == "year":
        return "YS"
    else:
        return None


def convenience_result_list_shortener(result: list[Any]) -> Union[list[Any], Any, None]:
    """
    Method used for convenience helpers to querying methods returning lists

    :param result: input list
    :return: Depends on the input list length:
        None if list is empty,
        unique list element if list has length one (i.e. returns X if input is [X], or
        input value if the list has length > 1
    """
    n_results = len(result)
    if n_results > 1:
        return result
    elif n_results == 0:
        return None
    else:
        return result[0]


def list_to_string(list2use: list, separator: str = ",") -> str:
    """
    Helper function to turn list into string, e.g. comma separated (default)

    :param list2use: input list to convert
    :param separator: separating character
    :return: string of elements separated by the separator
    """

    if isinstance(list2use, list):
        res = separator.join(map(str, list2use))
    else:
        raise TypeError("Input list2use must be a list")
    return res


def check_no_remaining_fields(d: dict, debug_helper: Optional[str]) -> None:
    """
    Helper to check for empty kwargs (to ensure adequate propagation)

    :param d: kwargs dictionary
    :param debug_helper: string message to help debugging
    :return: /
    """
    if DISPLAY_DEVELOPER_WARNING() and len(d) > 0:
        d_in = copy(d)
        [d_in.pop(key) for key, val in d.items() if val is None]

        if len(d_in) > 0:
            if debug_helper is not None:
                msg = (
                    "There are leftover fields in "
                    + debug_helper
                    + " to be implemented: "
                )
            else:
                msg = "There are leftover fields to be implemented: "

            warn(Warning(msg + str(d_in)))


def sanitise_unit_type_input(x: str) -> str:
    """
    Convenience function to fix specific unit types with unfortunate names in API

    :param x: input
    :return: API-compatible output
    """
    if x in ["localWeatherStation", "heatPump", "pv", "carCharger"]:
        y = x + "s"
    elif x in ["secondary"]:
        y = "secondaries"
    else:
        y = x
    return y
