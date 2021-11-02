import requests
from config import get_config, API_KEY, DEFAULT_LOCATION


def get_5_day(location, api_key):
	url = f'http://api.openweathermap.org/data/2.5/forecast?q={location}' \
			f'&units=imperial&appid={api_key}'
	return requests.get(url).json()


def get_default_data():
	config = get_config()
	return get_5_day(location=config[DEFAULT_LOCATION], api_key=config[API_KEY])
