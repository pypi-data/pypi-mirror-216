"""
Management control units and scheduling
"""
from typing import Any

import numpy as np
import pandas as pd
from requests.models import Response

from .building_unit import BaseBuildingUnit
from .helpers import check_no_remaining_fields
from .logging import Logging
from .setpoints import (
    InvalidScheduleError,
    get_setpoint_schedule,
    send_setpoint_schedule,
)
from .types import TYPE_DATETIME_INPUT


def validate_schedule(schedule_df: pd.DataFrame) -> None:
    """
    Method to validate a schedule (basically checking that there is no NaN or Inf data, and that the schedule is not empty)

    :param schedule_df: schedule to validate
    :raise: InvalidScheduleError if the schedule is invalid
    :return: /
    """
    if schedule_df["value"].isnull().any():
        raise InvalidScheduleError("requested schedule has missing values")
    if np.isinf(schedule_df["value"]).any():
        raise InvalidScheduleError("requested schedule has infinite values")
    if schedule_df.empty or (len(schedule_df) == 0):
        raise InvalidScheduleError(
            "An empty schedule_df was requested (the API does not accept this)"
        )


class ControlUnit(BaseBuildingUnit):
    """Control Unit; an extension of Unit to handle controls"""

    def __init__(self, unit_data: dict[str, Any], building_ref=None):
        super().__init__("control", unit_data, building_ref)
        if "active" in unit_data.keys():
            self.active = unit_data.pop("active")
        else:
            self.active = False

        check_no_remaining_fields(unit_data, debug_helper="control_unit_data")

    def request_schedule(self, schedule_df: pd.DataFrame) -> Response:
        """
        Sends a scheduling request to the API

        :param schedule_df: schedule to execute, as a DataFrame
        :return: requests.Response for the scheduling request
        """
        if self.active is False:
            Logging().warning(
                RuntimeWarning(
                    """Warning: you are trying to control an unit that is not activated 
                    (id={} / details: [unit: {} / building: [{}] {}])""".format(
                        self.id,
                        self.name,
                        self.building.location["locationId"],
                        self.building.location["address"],
                    )
                )
            )
        validate_schedule(schedule_df)
        return send_setpoint_schedule(self.id, schedule_df)

    def get_schedule(
        self, start_date: TYPE_DATETIME_INPUT, end_date: TYPE_DATETIME_INPUT
    ) -> pd.DataFrame:
        """
        Loads the past schedule for the unit and a given period

        :param start_date: start of the period
        :param end_date: end of the period
        :return: schedule in DataFrame format
        """
        return get_setpoint_schedule(self.id, start_date, end_date)
