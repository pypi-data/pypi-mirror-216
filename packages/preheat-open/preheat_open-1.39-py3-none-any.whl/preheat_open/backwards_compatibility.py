"""
Methods to ensure backwards-compatibility

The contents of this module will be deprecated in future versions
"""

from datetime import datetime

from preheat_open.logging import Logging

from .types import TYPE_DATETIME_INPUT


def warn_deprecation_pending(message: str) -> None:
    """
    Warns that a method/feature will be deprecated
    Note to developers: make sure to use this one as it streamlines the code and makes deprecation easily traceable

    :param message: message to print as warning
    """
    Logging().warning(DeprecationWarning(message))


def load_parameter_old_naming(
    start: TYPE_DATETIME_INPUT,
    end: TYPE_DATETIME_INPUT,
    resolution: str,
    postfix: str = "date",
    **kwargs,
) -> tuple[TYPE_DATETIME_INPUT, TYPE_DATETIME_INPUT, str]:
    """
    Checks for old parameter namings as start_date, end_date and time_resolution and forwards them to their respective
    new namings, i.e. start, end and resolution. Use by passing both new parameters down and a kwargs. Old namings will
    be caught and values passed on while a warning about the deprecation of the old namings is raised.
    """

    d = dict(start=start, end=end, resolution=resolution)
    for param, alt_name in {
        "start": f"start_{postfix}",
        "end": f"end_{postfix}",
        "resolution": "time_resolution",
    }.items():
        if alt_name in kwargs:
            d[param] = kwargs[alt_name]
            warn_deprecation_pending(
                f"Use of parameter '{alt_name}' is deprecated. Use '{param}' instead."
            )
    return d["start"], d["end"], d["resolution"]
