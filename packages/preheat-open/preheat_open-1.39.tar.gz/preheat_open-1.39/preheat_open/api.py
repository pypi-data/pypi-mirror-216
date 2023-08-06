"""
This module defines the basics of the interaction with Neogrid's web API
"""
import json
import os
from datetime import datetime
from io import StringIO
from typing import Any, Optional, Union

import numpy as np
import pandas as pd
from dateutil.tz import gettz
from requests import Session
from requests.adapters import HTTPAdapter
from requests.models import Response
from urllib3.util.retry import Retry

import preheat_open

from .backwards_compatibility import warn_deprecation_pending
from .exceptions import (  # For backwards compatibility
    AccessDeniedError,
    APIDataExtractError,
    APIKeyMissingError,
    MissingConfigurationFile,
    MissingConfigurationFileError,
)
from .logging import Logging, write_log_to_profiling_file
from .singleton import Singleton

# Settings of the API
BASE_URL: str = "https://api.neogrid.dk/public/api/v1"
MAX_CIDS_PER_REQ: int = 3
MAX_POINTS_PER_REQ: int = 90000
MAX_IDS_AND_CIDS_PER_REQUEST: int = 100
GET_TIMEOUT_SECONDS: int = 60
PUT_TIMEOUT_SECONDS: int = 10

# Perhaps we can steal this from the OS?
TIMEZONE = gettz("Europe/Copenhagen")
DATETIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S.%fZ"

# Addresses of the configuration file (if changing this, make sure to update the documentation in the README file
USER_LEVEL_CONFIGURATION_FILE: str = os.path.expanduser("~/.preheat/config.json")
MACHINE_LEVEL_CONFIGURATION_FILE: str = os.path.expanduser("/etc/preheat/config.json")
MACHINE_LEVEL_CONFIGURATION_FILE_OPT: str = os.path.expanduser(
    "/etc/opt/preheat/config.json"
)


def configuration_file_path() -> str:
    """
    Determines the path of the configuration file to be used.

    :raise: preheat_open.exceptions.MissingConfigurationFileError if no cofiguration file is available
    :return: full path of the configuration file
    """
    for i in [
        USER_LEVEL_CONFIGURATION_FILE,
        MACHINE_LEVEL_CONFIGURATION_FILE_OPT,
        MACHINE_LEVEL_CONFIGURATION_FILE,
    ]:
        if os.path.exists(i):
            return i
    raise MissingConfigurationFileError()


def api_string_to_datetime(t: str) -> datetime:
    """
    Converts a datetime string from the API to a python datetime

    :param t: datetime in string format
    :return: datetime corresponding to the input
    """
    return datetime.strptime(t, "%Y-%m-%dT%H:%M:%S.%f%z")


def datetime_to_api_string(t: datetime) -> str:
    """
    Converts a python datetime to a string ready for use in the API I/O

    :param t: datetime to convert to string
    :return: a string with a format compatible with the API
    """
    return t.isoformat()


def ids_list_to_string(list2use: list, separator: str = ",") -> str:
    """
    Helper function to turn list into string, e.g. comma separated (default).

    :param list2use: list to convert
    :param separator: separation character (default: ',')
    :return: list in string format
    """

    if isinstance(list2use, list):
        res = separator.join(map(str, list2use))
    elif isinstance(list2use, pd.Series):
        res = separator.join(map(str, list2use.to_list()))
    elif isinstance(list2use, np.ndarray):
        res = separator.join(map(str, list2use.tolist()))
    else:
        res = str(list2use)

    return res


def load_configuration() -> Union[None, dict]:
    """
    Loads the API configuration

    :return: None if no configuration file found, else a dictionary with the keys/values in the configuration file
    """
    config = None
    try:
        # Prefer config file in user home dir, else use the global config file
        config_file = configuration_file_path()
        if os.path.exists(config_file):
            Logging().info(f"Loading config from {config_file}")
            with open(config_file, "r") as fp:
                config = json.load(fp)
    except Exception:
        config = None

    return config


class ApiSession(metaclass=Singleton):
    """Singleton class to handle API connection sessions"""

    def __init__(self):
        # Adding protection against remote closing connection
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "PUT", "POST"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        http_session = Session()
        http_session.mount("https://", adapter)
        http_session.mount("http://", adapter)

        self.base_url = BASE_URL
        self.session = http_session
        Logging().debug(f"Creating API session [{self.addr()}]...")

        self.set_api_key()

    def addr(self) -> str:
        """
        Making a representation of the session object for use in logging

        :return: string representing the session
        """
        return hex(id(self.session))

    def get_api_key(self) -> str:
        """
        Getter for the API key of the user

        :return: the API key for the user
        """
        return self.session.headers.get("Authorization")

    def set_api_key(self, api_key: Optional[str] = None) -> None:
        """
        Sets the API key

        :param api_key: value of the API key (if None, loads from the configuration file)
        :return: /
        """
        if api_key is None:
            api_key = self._load_api_key(
                self.get_api_key().split(" ")[1]
                if self.get_api_key() is not None
                else None
            )
        else:
            Logging().debug(f"API key set manually [{self.addr()}]")
        headers = {"Authorization": "Apikey " + str(api_key)}
        self.session.headers.update(headers)

    def set_api_url(self, api_url=None):
        """
        DEPRECATED (only kept for backwards-compatibility)
        """
        warn_deprecation_pending(f"Manual update of the API url is deprecated")

    def __log_api_io(self, msg: str) -> None:
        Logging().debug(msg)
        write_log_to_profiling_file("API-I/O: " + msg)

    def api_get(
        self,
        endpoint: str,
        out: str = "json",
        payload: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, Any]] = None,
        bare_url: bool = False,
    ):
        """
        Method to send a GET request to the API

        :param endpoint: URL of the endpoint
        :param out: output type (json or csv)
        :param payload: payload for the request
        :param headers: headers to use for the request
        :param bare_url: if True, uses the endpoint as full URL (and skips base URL additions)
        :return: API response in request.Response format
        """
        payload = payload if payload is not None else {}
        headers = headers if headers is not None else {}
        self.__log_api_io(f"GET /{endpoint} [{self.addr()}]")

        if bare_url:
            path = endpoint
        else:
            path = self.base_url + "/" + endpoint

        if out == "csv":
            headers["Accept"] = "text/csv"
        resp = self.session.get(
            path, params=payload, headers=headers, timeout=GET_TIMEOUT_SECONDS
        )

        Logging().debug(f"{resp.status_code} {resp.reason}")
        try:
            resp.raise_for_status()
        except Exception as e:
            msg = """GET - FAILED
            URL: {}
            Payload: {}
            """.format(
                path, str(payload)
            )
            Logging().error(msg, exception=e)
            raise e

        try:
            if out == "json":
                return resp.json()
            elif out == "csv":
                data = StringIO(resp.text)
                return pd.read_csv(data, delimiter=";")
            else:
                raise ValueError("Invalid value for out parameter ({})".format(out))
        except ValueError as e:
            raise e
        except Exception as e:
            raise APIDataExtractError() from e

    def api_put(
        self,
        endpoint: str,
        out: str = "json",
        json_payload: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, Any]] = None,
        bare_url: bool = False,
    ) -> Response:
        """
        Method to send a PUT request to the API

        :param endpoint: URL of the endpoint
        :param out: output type (json or csv)
        :param json_payload: payload for the request
        :param headers: headers to use for the request
        :param bare_url: if True, uses the endpoint as full URL (and skips base URL additions)
        :return: API response in request.Response format
        """
        json_payload = json_payload if json_payload is not None else {}
        self.__log_api_io(f"PUT /{endpoint} [{self.addr()}]")

        if bare_url:
            path = endpoint
        else:
            path = self.base_url + "/" + endpoint
        r = self.session.put(path, json=json_payload, timeout=PUT_TIMEOUT_SECONDS)
        try:
            r.raise_for_status()
        except Exception as e:
            msg = """PUT - FAILED
            URL: {}
            Payload: {}
            """.format(
                path, str(json_payload)
            )
            Logging().error(msg, exception=e)
            raise e
        return r

    def api_post(
        self,
        endpoint: str,
        out: str = "json",
        json_payload: Optional[dict[str, Any]] = None,
        bare_url: bool = False,
    ) -> Response:
        """
        Method to send a POST request to the API

        :param endpoint: URL of the endpoint
        :param out: output type (json or csv)
        :param json_payload: payload for the request
        :param bare_url: if True, uses the endpoint as full URL (and skips base URL additions)
        :return: API response in request.Response format
        """
        json_payload = json_payload if json_payload is not None else {}
        self.__log_api_io(f"POST /{endpoint} [{self.addr()}]")

        if bare_url:
            path = endpoint
        else:
            path = self.base_url + "/" + endpoint
        r = self.session.post(path, json=json_payload, timeout=PUT_TIMEOUT_SECONDS)
        try:
            r.raise_for_status()
        except Exception as e:
            msg = """POST - FAILED
            URL: {}
            Payload: {}
            """.format(
                path, str(json_payload)
            )
            Logging().error(msg, exception=e)
            raise e
        return r

    def _load_api_key(self, existing: Optional[str]) -> str:
        """
        Load API key from environment variable
        - if API key not present in environment variable it will be set None
        - will then break when trying to access data on a building

        :param existing: the existing API key (None if not set)
        :return: the value of the API key
        """

        # First respect any override by set_api_key
        if os.environ.get("PREHEAT_API_KEY_OVERRIDE") is not None:
            if (
                existing is None
                or os.environ.get("PREHEAT_API_KEY_OVERRIDE") != existing
            ):
                Logging().info(f"Using API key from set_api_key() [{self.addr()}]")
            return os.environ.get("PREHEAT_API_KEY_OVERRIDE")

        # Else, try PREHEAT_API_KEY environment variable
        elif os.environ.get("PREHEAT_API_KEY") is not None:
            if existing is None or os.environ.get("PREHEAT_API_KEY") != existing:
                Logging().info(
                    f"Using API key from environment variable [{self.addr()}]"
                )
            return os.environ.get("PREHEAT_API_KEY")

        # Else, try loading configuration file
        else:
            # If config loaded, set API key accordingly to file
            if preheat_open.config is not None:
                config_keys = preheat_open.config.keys()
                if "API_KEY" in config_keys:
                    if existing is None or preheat_open.config["API_KEY"] != existing:
                        Logging().info(
                            f"Using API key from config file [{self.addr()}]"
                        )
                    return preheat_open.config["API_KEY"]
                elif "PREHEAT_API_KEY" in config_keys:
                    if (
                        existing is None
                        or preheat_open.config["PREHEAT_API_KEY"] != existing
                    ):
                        Logging().info(
                            f"Using API key from config file [{self.addr()}]"
                        )
                    return preheat_open.config["PREHEAT_API_KEY"]
                else:
                    raise Exception(
                        f"""Your configuration file is missing a 'PREHEAT_API_KEY' field"""
                    )

            # No environment variable, no config file, nothing we can do
            else:
                return str(None)

    def _load_api_url(self) -> str:
        """
        Loads the API url

        :return: the base URL of the API
        """
        if os.environ.get("PREHEAT_API_URL_OVERRIDE") is not None:
            url = os.environ.get("PREHEAT_API_URL_OVERRIDE")
            Logging().info(f"Using API url: {url} [{self.addr()}]")
            return url
        else:
            Logging().info(f"Using default API url [{self.addr()}]")
            return BASE_URL


def set_api_key(api_key: Optional[str]) -> None:
    """
    Sets the API key

    :param api_key: value of the API key
    :return: /
    """
    if api_key is None:
        if "PREHEAT_API_KEY_OVERRIDE" in os.environ:
            os.environ.pop("PREHEAT_API_KEY_OVERRIDE")
            Logging().info("API key override unset")
    else:
        os.environ["PREHEAT_API_KEY_OVERRIDE"] = api_key
        Logging().info("API key override set")
    ApiSession().set_api_key()


def api_get(
    endpoint: str,
    out: str = "json",
    payload: Optional[dict[str, Any]] = None,
    headers: Optional[dict[str, Any]] = None,
    bare_url: bool = False,
) -> Response:
    """
    Method to send a GET request to the API

    :param endpoint: URL of the endpoint
    :param out: output type (json or csv)
    :param payload: payload for the request
    :param headers: headers to use for the request
    :param bare_url: if True, uses the endpoint as full URL (and skips base URL additions)
    :return: API response in request.Response format
    """
    return ApiSession().api_get(
        endpoint,
        out=out,
        payload=payload,
        headers=headers,
        bare_url=bare_url,
    )


def api_post(
    endpoint: str,
    out: str = "json",
    json_payload: Optional[dict[str, Any]] = None,
    bare_url: bool = False,
) -> Response:
    """
    Method to send a POST request to the API

    :param endpoint: URL of the endpoint
    :param out: output type (json or csv)
    :param json_payload: payload for the request
    :param bare_url: if True, uses the endpoint as full URL (and skips base URL addition)
    :return: API response in request.Response format
    """
    return ApiSession().api_post(
        endpoint,
        out=out,
        json_payload=json_payload,
        bare_url=bare_url,
    )


def api_put(
    endpoint: str, json_payload: Optional[dict[str, Any]] = None, bare_url: bool = False
) -> Response:
    """
    Method to send a PUT request to the API

    :param endpoint: URL of the endpoint
    :param json_payload: payload for the request
    :param bare_url: if True, uses the endpoint as full URL (and skips base URL addition)
    :return: API response in request.Response format
    """
    return ApiSession().api_put(
        endpoint,
        out="json",
        json_payload=json_payload,
        bare_url=bare_url,
    )


# For backwards compatibility (deprecated methods and classes)
def set_api_url(api_url: str) -> None:
    """
    Only kept for backwards compatibility
    """
    warn_deprecation_pending(f"Manual update of the API url is deprecated")
    ApiSession().set_api_url(api_url)


def __enforce_imports():
    f = [APIKeyMissingError(), AccessDeniedError(), MissingConfigurationFile()]
