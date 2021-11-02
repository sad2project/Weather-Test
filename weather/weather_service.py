from datetime import date
from functools import partial
from itertools import groupby
from collections import Counter
from typing import Any, Callable, Iterable

from weather.data_mapper import map_json_list_to_weather
from weather.model import MessageType, Weather


def get_messaging_forecast(weather_forecast: list[dict]) -> list[tuple[date, MessageType]]:
    # first, maps the json list into Weather objects, then filters out data points that are too
    # early in the day or too late to be useful times to message. Lastly, it groups each data point
    # by its date
    data_points = filter_irrelevant_times(map_json_list_to_weather(weather_forecast))
    forecast = build_forecast(data_points)
    return forecast



def after_8am(data_point: Weather):
    return data_point.time().hour >= 8


def before_8pm(data_point: Weather):
    return data_point.time().hour < 20


def filter_irrelevant_times(data_points):
    for data_point in data_points:
        if after_8am(data_point) and before_8pm(data_point):
            yield data_point


def build_forecast(data_points):
    grouping = groupby(data_points, Weather.date)
    forecast = grouping_to_dict(grouping, map_to_messaging)
    return forecast


def grouping_to_dict(grouping, group_mapper: Callable[[Iterable[Weather]], Any]=list):
    out = {}
    for key, grp in grouping:
        group = list(grp)
        out[key] = group_mapper(group)
    return out


def map_to_messaging(hourly):
    hourly_message_types = map(Weather.message_type, hourly)
    message_type_count = Counter(hourly_message_types)
    return message_type_count.most_common(1)[0][0]  # chooses the most common message type. If there
    # are ties, it returns the first one to show up during the day.
