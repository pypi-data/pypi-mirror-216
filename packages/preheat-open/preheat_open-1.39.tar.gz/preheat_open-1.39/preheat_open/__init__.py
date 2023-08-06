"""
The preheat_open package provides methods to load building data from `Neogrids <https://www.neogrid.dk/>`_ platform
"""

# Imports for backwards compatibility of dependent code
# noinspection PyUnresolvedReferences
import os
import re
import sys

from . import _version
from .api import (
    BASE_URL,
    MAX_CIDS_PER_REQ,
    MAX_POINTS_PER_REQ,
    TIMEZONE,
    AccessDeniedError,
    APIDataExtractError,
    APIKeyMissingError,
    load_configuration,
    set_api_key,
)

# noinspection PyUnresolvedReferences
from .building import Building, available_buildings

# noinspection PyUnresolvedReferences
from .logging import set_logging_level

# noinspection PyUnresolvedReferences
from .unit import Unit

__version__ = _version.get_versions()["version"]


config = load_configuration()


def running_in_test_mode() -> bool:
    """
    Method to evaluate whether the code is running in test mode. Test mode is activated when using Pytest

    :return: True if running in test mode, False otherwise
    """
    # Pytest is detailed via argv or an environment variable
    if "PYTEST_CURRENT_TEST" in os.environ:
        return True
    elif any(re.findall(r"pytest|py.test", sys.argv[0])):
        return True
    else:
        return False


# list of environment variables for tricks
ENV_VAR_TRACK_MISSING_DATA_FIELD = "PREHEAT_OPEN_TRACK_MISSING_FIELDS"
