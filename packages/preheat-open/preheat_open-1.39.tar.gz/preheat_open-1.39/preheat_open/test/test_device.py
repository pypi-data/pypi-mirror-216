from pandas import DataFrame, Series

from preheat_open import test
from preheat_open.device import Device


class TestBuildingDevice(test.PreheatTest):
    def test_class(self, building_with_devices, short_period):
        devices = building_with_devices.devices

        def _validate_list(l):
            assert isinstance(l, list) and isinstance(l[0], Device) and (len(l) == 1)

        _validate_list(building_with_devices.query_devices(name="Fake test device"))
        _validate_list(building_with_devices.query_devices(device_type="HEAT_METER"))
        _validate_list(building_with_devices.query_devices(id=13255))
        _validate_list(
            building_with_devices.query_devices(
                name="Fake test device", device_type="HEAT_METER", id=13255
            )
        )

        assert (
            len(
                building_with_devices.query_devices(
                    name="Fake", device_type="HEAT_METER", id=13255
                )
            )
            == 0
        )
        assert (
            len(
                building_with_devices.query_devices(
                    name="Fake test device", device_type="0", id=13255
                )
            )
            == 0
        )
        assert (
            len(
                building_with_devices.query_devices(
                    name="Fake test device", device_type="HEAT_METER", id=1
                )
            )
            == 0
        )

        assert len(building_with_devices.query_devices(id=1)) == 0
        assert len(building_with_devices.query_devices(name="Does not exist")) == 0
        assert (
            len(building_with_devices.query_devices(device_type="Fake test device"))
            == 0
        )

        building_with_devices.load_device_data(*short_period)
        df0 = devices[0].data
        assert isinstance(df0, DataFrame)
        assert len(df0) > 1

        building_with_devices.clear_device_data()
        assert devices[0].data.empty

        s = devices[0].get_state(update=True, t_now=short_period[1])
        assert isinstance(s, Series) and len(s) > 0
