from copy import deepcopy

import pytest

import preheat_open
from preheat_open.test import (
    API_KEY,
    MEDIUM_TEST_PERIOD,
    SHORT_TEST_PERIOD,
    TEST_LOCATION_ID,
    mark_pytest_package_test,
)

# Defining fixture scope
FIXTURE_SCOPE = "session"


# Fixing API key once and for all
@pytest.fixture(autouse=True)
def mark_as_pytest_run():
    mark_pytest_package_test()


@pytest.fixture(autouse=True)
def set_api_key():
    preheat_open.api.set_api_key(API_KEY)


@pytest.fixture(scope=FIXTURE_SCOPE)
def medium_period():
    return MEDIUM_TEST_PERIOD


@pytest.fixture(scope=FIXTURE_SCOPE)
def short_period():
    return SHORT_TEST_PERIOD


@pytest.fixture(scope=FIXTURE_SCOPE)
def building():
    return preheat_open.Building(TEST_LOCATION_ID)


@pytest.fixture(scope=FIXTURE_SCOPE)
def building_with_devices(building):
    b = deepcopy(building)
    b.load_devices()
    return b


@pytest.fixture(scope=FIXTURE_SCOPE)
def building_with_data(building, medium_period):
    building_new = deepcopy(building)
    building_new.load_data(*medium_period)
    return building_new


# Legacy fixtures
@pytest.fixture(scope=FIXTURE_SCOPE)
def building_id():
    return TEST_LOCATION_ID


@pytest.fixture(scope=FIXTURE_SCOPE)
def unit_id():
    return 15312


@pytest.fixture(scope=FIXTURE_SCOPE)
def control_unit_id():
    return 15357


@pytest.fixture(scope=FIXTURE_SCOPE)
def unit(building, unit_id):
    return building.query_units(unit_id=unit_id)[0]


@pytest.fixture(scope=FIXTURE_SCOPE)
def unit_with_data(unit, medium_period):
    unit_new = deepcopy(unit)
    unit_new.load_data(*medium_period)
    return unit_new


@pytest.fixture(scope=FIXTURE_SCOPE)
def control_unit(building):
    return building.qu("control", "control_unit_custom_1")


@pytest.fixture(scope=FIXTURE_SCOPE)
def weather_unit(building):
    return building.weather
