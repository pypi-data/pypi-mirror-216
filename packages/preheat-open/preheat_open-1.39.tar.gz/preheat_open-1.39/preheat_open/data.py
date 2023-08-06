"""
To manage timeseries data loading
"""
import math
from datetime import datetime, timedelta
from functools import reduce
from typing import Any, Optional

import numpy as np
import pandas as pd

from .api import (
    DATETIME_FORMAT,
    MAX_IDS_AND_CIDS_PER_REQUEST,
    MAX_POINTS_PER_REQ,
    APIDataExtractError,
    api_get,
    datetime_to_api_string,
)
from .helpers import list_to_string, sanitise_datetime_input
from .types import TYPE_DATETIME_INPUT

__DEFAULT_DATAFRAME_INDEX = pd.DatetimeIndex([], tz="UTC")


def load_box_data(
    component_map: dict[str, Any],
    start: TYPE_DATETIME_INPUT,
    end: TYPE_DATETIME_INPUT,
    resolution="minute",
) -> pd.DataFrame:
    """
    Loads box data from the API

    :param component_map: mapping of the components to load data for
    :param start: start of the period
    :param end: end of the period
    :param resolution: resolution to load data with (raw, minute/5min, hour , day, week, month, year)
    :return: data in Dataframe format
    """
    start = sanitise_datetime_input(start)
    end = sanitise_datetime_input(end)
    __check_start_end_date(start, end)

    path = "measurements"
    cid_key = "cids"
    cids = list(component_map.keys())

    if not cids:
        return pd.DataFrame(data={}, index=__DEFAULT_DATAFRAME_INDEX)

    resp = __perform_requests(path, cid_key, cids, start, end, resolution, "csv")

    return __extract_data(resp, "cid", component_map, "csv").astype(float)


def load_model_data(
    component_map: dict[str, Any],
    start: TYPE_DATETIME_INPUT,
    end: TYPE_DATETIME_INPUT,
    resolution="raw",
) -> pd.DataFrame:
    """
    Loads data using a building model representation

    :param component_map: mapping of the components
    :param start: start of the period
    :param end: end of the period
    :param resolution: resolution of the data (raw, minute/5min, hour, day, week, month, year)
    :return: data loaded in dataFrame format
    """
    start = sanitise_datetime_input(start)
    end = sanitise_datetime_input(end)
    __check_start_end_date(start, end)

    path = "units/measurements"
    id_key = "ids"
    ids = list(component_map.keys())

    if not ids or len(ids) == 0:
        return pd.DataFrame(data={}, index=__DEFAULT_DATAFRAME_INDEX)

    if resolution != "raw":
        # Do chunked requests
        resp = __perform_requests(path, id_key, ids, start, end, resolution, "csv")
    else:
        # Do single request
        resp = __make_request(path, {id_key: ids}, start, end, resolution, "csv")

    return __extract_data(resp, "id", component_map, "csv").astype(float)


def load_weather_data(
    location_id: int,
    component_map: dict[str, Any],
    start: TYPE_DATETIME_INPUT,
    end: TYPE_DATETIME_INPUT,
    resolution: str = "hour",
    **kwargs,
) -> pd.DataFrame:
    """
    Loads weather data from the API

    :param location_id: location ID
    :param component_map: mapping of the components
    :param start: start of the period
    :param end: end of the period
    :param resolution: resolution of the data (raw, minute/5min, hour, day, week, month, year)
        Note: raw, minute/5min are overwritten to hour
    :param kwargs: /
    :return: loaded data in DataFrame format
    """
    # Parse strings to datetime object
    start = sanitise_datetime_input(start)
    end = sanitise_datetime_input(end)
    __check_start_end_date(start, end)

    path = f"weather/{location_id}"
    cid_key = "type_ids"
    cids = list(component_map.keys())

    # If minutes, then we need to resample
    if resolution in ["minute", "5min", "raw"]:
        resolution = "hour"
        t_span = (start - timedelta(hours=1), end + timedelta(hours=1), resolution)
        resample = True
    else:
        t_span = (start, end, resolution)
        resample = False

    resp = __perform_requests(path, cid_key, cids, *t_span, "csv")

    if resample:
        return (
            __extract_data(resp, "type_id", component_map, "csv")
            .resample("5min")
            .ffill()[start:end]
        )

    return __extract_data(resp, "type_id", component_map, "csv").astype(float)


def perform_requests(
    path,
    cid_key,
    cids,
    start: TYPE_DATETIME_INPUT,
    end: TYPE_DATETIME_INPUT,
    resolution: str,
    format: str = "csv",
):
    return __perform_requests(path, cid_key, cids, start, end, resolution, format)


def __perform_requests(
    path,
    cid_key,
    cids,
    start: TYPE_DATETIME_INPUT,
    end: TYPE_DATETIME_INPUT,
    resolution: str,
    format: str = "csv",
):
    # Split CIDs into chunks
    # NOTE: we reduce number of CIDs pr. REQ to confine w. MAX_POINTS_PER_REQ
    # This sets the limit to 90000 points on a single CID; which for 5min.
    # is roughly 300 days of data.
    time_lookup = {
        "raw": 10,
        "minute": 300,
        "5min": 300,
        "hour": 3600,
        "day": 86400,
        "week": 604800,
        "month": 16934400,
        "year": 6181056000,
    }

    end_date_in = sanitise_datetime_input(end)
    start_date_in = sanitise_datetime_input(start)

    dt = end_date_in - start_date_in

    N_points_requested = len(cids) * dt.total_seconds() / time_lookup[resolution]

    if N_points_requested < 1:
        reqs = []
    else:
        cid_chunk_size = (MAX_POINTS_PER_REQ / N_points_requested) * len(cids)

        # Imposing another max of number of IDs and CIDs regardless of resolution
        cid_chunk_size = min(cid_chunk_size, MAX_IDS_AND_CIDS_PER_REQUEST)

        cid_chunks = [
            cids[x : x + max(int(cid_chunk_size), 1)]
            for x in range(0, len(cids), max(int(cid_chunk_size), 1))
        ]
        time_chunks = math.ceil(1 / cid_chunk_size)
        dt_chunk = (end_date_in - start_date_in) / np.fmax(1, time_chunks)

        reqs = []
        for cid_chunk in cid_chunks:
            for i in range(time_chunks):
                reqs.append(
                    __make_request(
                        path,
                        {cid_key: list_to_string(cid_chunk)},
                        start + i * dt_chunk,
                        start + (i + 1) * dt_chunk,
                        resolution,
                        format,
                    )
                )

    return reqs


def __make_request(
    path, payload, start: datetime, end: datetime, resolution: str, format: str = "csv"
):
    payload["start_time"] = datetime_to_api_string(start)
    payload["end_time"] = datetime_to_api_string(end)

    if resolution == "5min":
        resolution = "minute"

    payload["time_resolution"] = resolution

    return api_get(path, payload=payload, out=format)


def extract_data(resp, id_key, component_map, format: str = "csv"):
    return __extract_data(resp, id_key, component_map, format)


def __reformat_dataframe(
    resp: pd.DataFrame,
    component_map: dict[str, str],
    id_key: Optional[str] = None,
) -> pd.DataFrame:
    kwargs_to_datetime = dict(utc=True, format=DATETIME_FORMAT)
    # If this is having an issue, use "infer_datetime_format=True" instead of "format=..."

    # Use of resp.loc["time"] was removed below as it triggers warnings for pandas>=1.5
    resp["time"] = pd.to_datetime(resp["time"], **kwargs_to_datetime)

    resp_columns = resp.keys()
    if id_key is not None:
        components = id_key
    elif "id" in resp_columns:
        components = "id"
    elif "type_id" in resp_columns:
        components = "type_id"
    else:
        raise RuntimeError("Unknown column formatting")
    comp_map_rename = {int(i): component_map[i] for i in component_map}
    component_names = comp_map_rename.values()
    if resp.empty:
        # For backwards compatibility
        out = pd.DataFrame(
            {i: [] for i in component_names}, index=__DEFAULT_DATAFRAME_INDEX
        )
    else:
        out = resp.pivot(index="time", columns=components, values="value").rename(
            columns=comp_map_rename,
        )

    for c in component_names:
        if c not in out.keys():
            out[c] = np.nan

    out.axes[1].name = None  # For backwards compatibility
    return out


def __extract_data(resp, id_key, component_map, format="csv"):
    if len(resp) < 1:
        # Short circuit all in case of empty response
        out = pd.DataFrame(
            {i: [] for i in component_map.values()}, index=__DEFAULT_DATAFRAME_INDEX
        )
    elif format == "json":
        if isinstance(resp, list):
            # Initialize empty response that we can append to
            resp_new = {cid: [] for cid in component_map.keys()}
            for req in resp:
                for cid, values in req.items():
                    resp_new[cid] += values
            resp = resp_new

        if "message" in resp:
            raise APIDataExtractError(resp["message"])

        kwargs_to_datetime = dict(utc=True, format=DATETIME_FORMAT)
        dfs = []
        for cid, name in component_map.items():
            time = pd.to_datetime(
                [data["time"] for data in resp[cid]], **kwargs_to_datetime
            )
            value = [data["value"] for data in resp[cid]]

            df_i = pd.DataFrame(value, columns=[name], index=time)
            dfs.append(df_i)

        out = reduce(
            lambda x, y: pd.merge(x, y, left_index=True, right_index=True, how="outer"),
            dfs,
        )

    elif format == "csv":
        # Join response into one
        if isinstance(resp, list):
            resp_new = None
            for df in resp:
                resp_new = df if resp_new is None else pd.concat([resp_new, df])
            resp = resp_new

        out = __reformat_dataframe(resp, component_map, id_key)

    elif format == "dataframe":
        out = __reformat_dataframe(resp, component_map, id_key)

    else:
        raise TypeError("Unsupported format")

    out.index.rename(None, inplace=True)
    return out


def __check_start_end_date(start: datetime, end: datetime) -> None:
    if end < start:
        raise ValueError("End date must be AFTER start date")
