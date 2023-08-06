import pandas as pd
from requests import HTTPError
from requests.models import Response

from .api import TIMEZONE, api_get, api_put
from .exceptions import InvalidSchedule  # For backwards compatibility
from .exceptions import InvalidScheduleError
from .helpers import sanitise_datetime_input
from .types import TYPE_DATETIME_INPUT


def send_setpoint_schedule(controlunit_id: int, schedule_df: pd.DataFrame) -> Response:
    path = f"controlunit/{controlunit_id}/setpoint"

    # Build payload from DataFrame
    payload = {"schedule": []}
    if "operation" not in schedule_df.keys():
        schedule_df["operation"] = len(schedule_df) * ["NORMAL"]

    [
        payload["schedule"].append(
            {
                "startTime": index.isoformat(),
                "value": row["value"],
                "operation": row["operation"],
            }
        )
        for index, row in schedule_df.iterrows()
    ]

    try:
        # PUT request
        return api_put(path, json_payload=payload)
    except HTTPError as e:
        extra_info = f"""HTTP error when writing the schedule: 
            {str(payload["schedule"])}
            
            Details: {e}"""
        raise InvalidScheduleError(extra_info) from e


def get_setpoint_schedule(
    controlunit_id: int, start_date: TYPE_DATETIME_INPUT, end_date: TYPE_DATETIME_INPUT
) -> pd.DataFrame:
    start_date = sanitise_datetime_input(start_date)
    end_date = sanitise_datetime_input(end_date)

    path = f"controlunit/{controlunit_id}/setpoint"

    payload = {
        "start_time": start_date.isoformat(),
        "end_time": end_date.isoformat(),
    }

    raw = api_get(path, out="json", payload=payload)
    df = pd.DataFrame(raw)

    if df.empty:
        return df

    df["startTime"] = pd.to_datetime(df["startTime"], utc=True)
    return df.set_index("startTime")


# For backwards compatibility
def __enforce_imports():
    d = [InvalidSchedule(), TIMEZONE]
