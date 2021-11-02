from datetime import datetime

from weather.model import Weather


def map_json_list_to_weather(json):
        return map(from_json_to_weather, json)


def from_json_to_weather(json):
    dt = parse_datetime(json['dt_txt'])
    temp = float(json['main']['temp'])
    condition = json['weather'][0]['main']
    return Weather(dt, temp, condition)


DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


def parse_datetime(dt_str: str) -> datetime:
    return datetime.strptime(dt_str, DATE_FORMAT)