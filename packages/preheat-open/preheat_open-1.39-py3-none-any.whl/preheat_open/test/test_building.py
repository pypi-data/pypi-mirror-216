from copy import deepcopy

import networkx as nx
import pandas as pd

from preheat_open import test
from preheat_open.weather import Weather


class TestBuilding(test.PreheatTest):
    def test_building(self, building):
        assert building is not None
        assert building.weather is not None
        assert isinstance(building.weather, Weather)
        assert building.units is not None
        assert len(building.units) > 0
        assert building.units["heating"] is not None

    def test_query_units(self, building, unit_id):
        assert building.query_units(unit_id=unit_id) is not None
        assert building.query_units("heating") is not None
        assert building.query_units("heating", exclude_shared=True) is not None
        assert building.query_units("?h") is not None
        assert building.query_units("?ting") is not None
        assert building.qu(name="heating_primary") is not None

        assert building.query_units("definitely not there") is not None
        assert len(building.query_units("definitely not there")) == 0
        assert building.qu(name="definitely not there") is None
        assert building.qu(unit_id="definitely not there") is None

    def test_unit_graph(self, building):
        g = building.unit_graph
        assert g is not None
        assert isinstance(g, nx.MultiDiGraph)

    def test_clear_data(self, building_with_data):
        from copy import deepcopy

        building_new = deepcopy(building_with_data)
        building_new.clear_data()
        assert building_new.weather is not None
        assert building_new.weather.data is not None
        assert building_new.weather.data.empty

    def test_load_data(self, building_with_data, short_period):
        # Testing standard data loading
        assert building_with_data is not None
        assert building_with_data.weather is not None
        assert building_with_data.weather.data is not None
        assert not building_with_data.weather.data.empty

        # Testing selective data loading
        new_building_with_data = deepcopy(building_with_data)
        new_building_with_data.clear_data()
        comps = {
            "weather": ["Temperature", "Humidity"],
            "main": None,
            "secondaries": ["supplyT"],
        }
        new_building_with_data.load_data(*short_period, components=comps)

        df_weather = new_building_with_data.weather.data
        df_main = new_building_with_data.query_units("main")[0].data
        df_secondary = new_building_with_data.query_units("secondaries")[0].data

        assert df_weather.empty is False
        assert "Temperature" in df_weather
        assert "Humidity" in df_weather
        assert "WindSpeed" not in df_weather

        assert df_main.empty is False

        assert df_secondary.empty is False
        assert "supplyT" in df_secondary
        assert "returnT" not in df_secondary

        assert new_building_with_data.query_units("indoorClimate")[0].data.empty is True
        assert new_building_with_data.query_units("heating")[0].data.empty is True

    def test_get_sub_zones(self, building_with_data):
        assert building_with_data.get_zones([]) == []
        assert len(building_with_data.get_zones([1])) == 0
        assert len(building_with_data.get_zones([4830])) == 1
        assert len(building_with_data.get_zones([4830, 4834])) == 2
        assert len(building_with_data.query_zones(zone_id=0)) == 0
        assert len(building_with_data.query_zones(zone_id=4830)) == 1
        assert len(building_with_data.query_zones(zone_type="apartment")) >= 1
        assert (
            len(building_with_data.query_zones(zone_id=4830, zone_type="apartment"))
            == 1
        )
        assert (
            len(building_with_data.query_zones(zone_id=4830, zone_type="doesnt exist"))
            == 0
        )
        assert len(building_with_data.query_zones(zone_type="doesnt exist")) == 0

    def test_describe(self, building_with_devices):
        assert isinstance(building_with_devices.describe(display=False), str)
        assert isinstance(building_with_devices.describe_devices(display=False), str)


def test_available_buildings():
    from preheat_open.building import available_buildings

    df = available_buildings()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1, "The API key has access to too many buildings"
