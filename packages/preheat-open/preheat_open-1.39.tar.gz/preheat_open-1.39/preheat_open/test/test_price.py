import pytest

from preheat_open import test
from preheat_open.helpers import now, timedelta


class TestPrice(test.PreheatTest):
    def test_building(self, building):
        assert building is not None

        sps = building.get_supply_points()
        assert sps is not None, "Failure in supply points"

        comps = sps[0].get_price_components()
        assert comps is not None, "Failure in price components extraction"

        # Test backwards compatibility
        with pytest.warns(DeprecationWarning):
            sps[0].load_price_data(start_time=now() - timedelta(days=1), end_time=now())
            data, df = sps[0].get_price_data()
            assert data is not None, "Failure in data"
            assert df is not None, "Failure in data labelling"

        sps[0].clear_price_data()
        sps[0].load_price_data(start=now() - timedelta(days=1), end=now())
        data2, df2 = sps[0].get_price_data()
        assert data2 is not None, "Failure in data"
        assert df2 is not None, "Failure in data labelling"
