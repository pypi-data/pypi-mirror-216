from typing import Optional

import pandas as pd

from .backwards_compatibility import load_parameter_old_naming
from .component import Component
from .data import load_weather_data
from .helpers import check_no_remaining_fields, now, sanitise_datetime_input, timedelta
from .types import TYPE_DATETIME_INPUT
from .unit import Unit


class Weather(Unit):
    """Weather; an extension of Unit to handle Weather extraction"""

    def __init__(self, location_id, weather_data):
        super().__init__("weather", weather_data)
        self.location_id = location_id
        self.id = weather_data.pop("gridId", None)
        self.name = "WeatherForecast"

        [
            self.components.append(Component(type_i))
            for type_i in weather_data.pop("types")
        ]
        check_no_remaining_fields(weather_data, debug_helper="weather_unit_data")

    def load_data(
        self,
        start: TYPE_DATETIME_INPUT,
        end: TYPE_DATETIME_INPUT,
        resolution: str = "hour",
        components=None,
        **kwargs
    ) -> None:
        # Parse strings to datetime object

        start, end, resolution = load_parameter_old_naming(
            start, end, resolution, **kwargs
        )

        start = sanitise_datetime_input(start)
        end = sanitise_datetime_input(end)

        self._warn_if_data_is_loaded()
        components_to_load = self.get_all_component_ids(components=components)
        if components is not None:
            components_to_load = {
                k: components_to_load[k]
                for k in components_to_load
                if components_to_load[k] in components
            }

        if (end - start) > pd.Timedelta("180d"):
            # Batch in 6M intervals (max we can load at a time)
            parts = list(pd.date_range(start=start, end=end, freq="180d"))

            if start != parts[0]:
                parts.insert(0, start)
            if end != parts[-1]:
                parts.append(end)

            parts[0] -= pd.Timedelta("1d")  # we add back one day later

            if parts[-1] - parts[-2] < pd.Timedelta("1d"):
                parts[-2] -= pd.Timedelta("1d")

            pairs = zip(map(lambda d: d + pd.Timedelta("1d"), parts[:-1]), parts[1:])

            dfs = [
                load_weather_data(
                    self.location_id,
                    components_to_load,
                    start,
                    end,
                    resolution,
                )
                for start, end in pairs
            ]
            res = pd.concat(dfs)

        else:
            res = load_weather_data(
                self.location_id,
                components_to_load,
                start,
                end,
                resolution,
            )

        self.data: pd.DataFrame = res
        self._ensure_continuity_of_data(resolution)

    def load_state(
        self,
        seconds_back: int = 3600,
        t_now=None,
        resolution_overwrite: Optional[str] = None,
    ) -> None:
        t_now = now() if t_now is None else sanitise_datetime_input(t_now)

        if resolution_overwrite is None:
            resolution = "hour"
        else:
            resolution = resolution_overwrite

        components_to_load = self.get_all_component_ids()
        self._state = load_weather_data(
            self.location_id,
            components_to_load,
            t_now - timedelta(seconds=seconds_back),
            t_now,
            resolution,
        )

    def get_state(
        self,
        update: bool = False,
        estimate: str = "last",
        seconds_back: int = 3600,
        resolution_overwrite: Optional[str] = None,
        **kwargs
    ) -> pd.Series:
        return super().get_state(
            update=update,
            estimate=estimate,
            seconds_back=seconds_back,
            resolution_overwrite=resolution_overwrite,
            **kwargs
        )
