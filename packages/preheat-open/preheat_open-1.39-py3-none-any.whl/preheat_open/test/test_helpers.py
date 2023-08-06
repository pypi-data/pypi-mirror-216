from preheat_open.helpers import (
    convenience_result_list_shortener,
    sanitise_unit_type_input,
)


def test_sanitisation():
    assert sanitise_unit_type_input("heatPumps") == "heatPumps"
    assert sanitise_unit_type_input("localWeatherStations") == "localWeatherStations"

    # Test those with actual changes
    assert sanitise_unit_type_input("heatPump") == "heatPumps"
    assert sanitise_unit_type_input("localWeatherStation") == "localWeatherStations"
    assert sanitise_unit_type_input("secondary") == "secondaries"


def test_convenience():
    assert convenience_result_list_shortener([]) is None
    assert convenience_result_list_shortener([123]) == 123
    assert convenience_result_list_shortener([123, 456]) == [123, 456]
    assert convenience_result_list_shortener([123, 456, 789]) == [123, 456, 789]
