from datetime import date, datetime
from unittest import TestCase

from weather.data_mapper import map_json_list_to_weather
from weather.model import MessageType, Weather
from weather.weather_service import filter_irrelevant_times, get_messaging_forecast

data = [
	# Nov 2, 2021;
	{'dt': 1635832800, 'main': {'temp': 64.07, 'feels_like': 27.68, 'temp_min': 34.07, 'temp_max': 34.07, 'pressure': 1028, 'sea_level': 1028, 'grnd_level': 997, 'humidity': 65, 'temp_kf': 0}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03n'}], 'clouds': {'all': 41}, 'wind': {'speed': 7.49, 'deg': 303, 'gust': 19.1}, 'visibility': 10000, 'pop': 0, 'sys': {'pod': 'n'}, 'dt_txt': '2021-11-02 06:00:00'},
	{'dt': 1635843600, 'main': {'temp': 62.38, 'feels_like': 26.01, 'temp_min': 32.38, 'temp_max': 32.38, 'pressure': 1029, 'sea_level': 1029, 'grnd_level': 997, 'humidity': 70, 'temp_kf': 0}, 'weather': [{'id': 800, 'main': 'Drizzle', 'description': 'clear sky', 'icon': '01n'}], 'clouds': {'all': 7}, 'wind': {'speed': 6.93, 'deg': 303, 'gust': 18.72}, 'visibility': 10000, 'pop': 0, 'sys': {'pod': 'n'}, 'dt_txt': '2021-11-02 09:00:00'},
	{'dt': 1635854400, 'main': {'temp': 61.44, 'feels_like': 25.23, 'temp_min': 31.44, 'temp_max': 31.44, 'pressure': 1030, 'sea_level': 1030, 'grnd_level': 998, 'humidity': 69, 'temp_kf': 0}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'clouds': {'all': 5}, 'wind': {'speed': 6.44, 'deg': 306, 'gust': 18.39}, 'visibility': 10000, 'pop': 0, 'sys': {'pod': 'n'}, 'dt_txt': '2021-11-02 12:00:00'},
	{'dt': 1635865200, 'main': {'temp': 64.5, 'feels_like': 29.05, 'temp_min': 34.5, 'temp_max': 34.5, 'pressure': 1031, 'sea_level': 1031, 'grnd_level': 999, 'humidity': 59, 'temp_kf': 0}, 'weather': [{'id': 802, 'main': 'Rain', 'description': 'scattered clouds', 'icon': '03d'}], 'clouds': {'all': 34}, 'wind': {'speed': 6.22, 'deg': 312, 'gust': 11.72}, 'visibility': 10000, 'pop': 0, 'sys': {'pod': 'd'}, 'dt_txt': '2021-11-02 15:00:00'},
	{'dt': 1635876000, 'main': {'temp': 60.48, 'feels_like': 35.76, 'temp_min': 40.48, 'temp_max': 40.48, 'pressure': 1029, 'sea_level': 1029, 'grnd_level': 998, 'humidity': 42, 'temp_kf': 0}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02d'}], 'clouds': {'all': 24}, 'wind': {'speed': 6.91, 'deg': 305, 'gust': 10.56}, 'visibility': 10000, 'pop': 0, 'sys': {'pod': 'd'}, 'dt_txt': '2021-11-02 18:00:00'},
	{'dt': 1635886800, 'main': {'temp': 62.31, 'feels_like': 37.76, 'temp_min': 42.31, 'temp_max': 42.31, 'pressure': 1028, 'sea_level': 1028, 'grnd_level': 997, 'humidity': 37, 'temp_kf': 0}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04d'}], 'clouds': {'all': 88}, 'wind': {'speed': 7.29, 'deg': 305, 'gust': 10.51}, 'visibility': 10000, 'pop': 0, 'sys': {'pod': 'd'}, 'dt_txt': '2021-11-02 21:00:00'},
	# Nov 3, 2021
	{'dt': 1635919200, 'main': {'temp': 34.84, 'feels_like': 34.84, 'temp_min': 34.84, 'temp_max': 34.84, 'pressure': 1030, 'sea_level': 1030, 'grnd_level': 999, 'humidity': 53, 'temp_kf': 0}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'clouds': {'all': 6}, 'wind': {'speed': 2.39, 'deg': 321, 'gust': 3.42}, 'visibility': 10000, 'pop': 0, 'sys': {'pod': 'n'}, 'dt_txt': '2021-11-03 06:00:00'},
	{'dt': 1635930000, 'main': {'temp': 83.71, 'feels_like': 33.71, 'temp_min': 33.71, 'temp_max': 33.71, 'pressure': 1030, 'sea_level': 1030, 'grnd_level': 999, 'humidity': 56, 'temp_kf': 0}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'clouds': {'all': 6}, 'wind': {'speed': 0.78, 'deg': 332, 'gust': 1.01}, 'visibility': 10000, 'pop': 0, 'sys': {'pod': 'n'}, 'dt_txt': '2021-11-03 09:00:00'},
	{'dt': 1635940800, 'main': {'temp': 82.86, 'feels_like': 32.86, 'temp_min': 32.86, 'temp_max': 32.86, 'pressure': 1030, 'sea_level': 1030, 'grnd_level': 998, 'humidity': 59, 'temp_kf': 0}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'clouds': {'all': 7}, 'wind': {'speed': 1.99, 'deg': 233, 'gust': 2.24}, 'visibility': 10000, 'pop': 0, 'sys': {'pod': 'n'}, 'dt_txt': '2021-11-03 12:00:00'},
	{'dt': 1635951600, 'main': {'temp': 76.19, 'feels_like': 36.19, 'temp_min': 36.19, 'temp_max': 36.19, 'pressure': 1031, 'sea_level': 1031, 'grnd_level': 999, 'humidity': 52, 'temp_kf': 0}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03d'}], 'clouds': {'all': 34}, 'wind': {'speed': 2.95, 'deg': 211, 'gust': 4.59}, 'visibility': 10000, 'pop': 0, 'sys': {'pod': 'd'}, 'dt_txt': '2021-11-03 15:00:00'},
	{'dt': 1635962400, 'main': {'temp': 81.4, 'feels_like': 38.7, 'temp_min': 41.4, 'temp_max': 41.4, 'pressure': 1030, 'sea_level': 1030, 'grnd_level': 998, 'humidity': 40, 'temp_kf': 0}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'clouds': {'all': 65}, 'wind': {'speed': 4.27, 'deg': 214, 'gust': 6.11}, 'visibility': 10000, 'pop': 0, 'sys': {'pod': 'd'}, 'dt_txt': '2021-11-03 18:00:00'},
	{'dt': 1635973200, 'main': {'temp': 44.26, 'feels_like': 42.28, 'temp_min': 44.26, 'temp_max': 44.26, 'pressure': 1027, 'sea_level': 1027, 'grnd_level': 996, 'humidity': 34, 'temp_kf': 0}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03d'}], 'clouds': {'all': 38}, 'wind': {'speed': 3.96, 'deg': 236, 'gust': 6.53}, 'visibility': 10000, 'pop': 0, 'sys': {'pod': 'd'}, 'dt_txt': '2021-11-03 21:00:00'},
	# Nov 4, 2021
	{'dt': 1636005600, 'main': {'temp': 37.18, 'feels_like': 34.16, 'temp_min': 37.18, 'temp_max': 37.18, 'pressure': 1026, 'sea_level': 1026, 'grnd_level': 995, 'humidity': 52, 'temp_kf': 0}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02n'}], 'clouds': {'all': 11}, 'wind': {'speed': 3.91, 'deg': 184, 'gust': 9.01}, 'visibility': 10000, 'pop': 0, 'sys': {'pod': 'n'}, 'dt_txt': '2021-11-04 06:00:00'},
	{'dt': 1636016400, 'main': {'temp': 76.23, 'feels_like': 33.46, 'temp_min': 36.23, 'temp_max': 36.23, 'pressure': 1025, 'sea_level': 1025, 'grnd_level': 994, 'humidity': 65, 'temp_kf': 0}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}], 'clouds': {'all': 64}, 'wind': {'speed': 3.53, 'deg': 207, 'gust': 8.48}, 'visibility': 10000, 'pop': 0, 'sys': {'pod': 'n'}, 'dt_txt': '2021-11-04 09:00:00'},
	{'dt': 1636027200, 'main': {'temp': 75.62, 'feels_like': 32.56, 'temp_min': 35.62, 'temp_max': 35.62, 'pressure': 1025, 'sea_level': 1025, 'grnd_level': 993, 'humidity': 83, 'temp_kf': 0}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03n'}], 'clouds': {'all': 45}, 'wind': {'speed': 3.71, 'deg': 214, 'gust': 10.13}, 'visibility': 10000, 'pop': 0, 'sys': {'pod': 'n'}, 'dt_txt': '2021-11-04 12:00:00'},
	{'dt': 1636038000, 'main': {'temp': 69.97, 'feels_like': 36.12, 'temp_min': 39.97, 'temp_max': 39.97, 'pressure': 1024, 'sea_level': 1024, 'grnd_level': 993, 'humidity': 69, 'temp_kf': 0}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'clouds': {'all': 6}, 'wind': {'speed': 5.44, 'deg': 216, 'gust': 11.25}, 'visibility': 10000, 'pop': 0, 'sys': {'pod': 'd'}, 'dt_txt': '2021-11-04 15:00:00'},
	{'dt': 1636048800, 'main': {'temp': 78.7, 'feels_like': 45.54, 'temp_min': 48.7, 'temp_max': 48.7, 'pressure': 1023, 'sea_level': 1023, 'grnd_level': 992, 'humidity': 54, 'temp_kf': 0}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'clouds': {'all': 6}, 'wind': {'speed': 7.18, 'deg': 223, 'gust': 12.84}, 'visibility': 10000, 'pop': 0, 'sys': {'pod': 'd'}, 'dt_txt': '2021-11-04 18:00:00'}, {'dt': 1636059600, 'main': {'temp': 52, 'feels_like': 49.01, 'temp_min': 52, 'temp_max': 52, 'pressure': 1020, 'sea_level': 1020, 'grnd_level': 990, 'humidity': 45, 'temp_kf': 0}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'clouds': {'all': 5}, 'wind': {'speed': 8.5, 'deg': 220, 'gust': 12.66}, 'visibility': 10000, 'pop': 0, 'sys': {'pod': 'd'}, 'dt_txt': '2021-11-04 21:00:00'},
	# Nov 5, 2021
	{'dt': 1636092000, 'main': {'temp': 43, 'feels_like': 38.64, 'temp_min': 43, 'temp_max': 43, 'pressure': 1020, 'sea_level': 1020, 'grnd_level': 989, 'humidity': 66, 'temp_kf': 0}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'clouds': {'all': 1}, 'wind': {'speed': 7.2, 'deg': 193, 'gust': 23.73}, 'visibility': 10000, 'pop': 0, 'sys': {'pod': 'n'}, 'dt_txt': '2021-11-05 06:00:00'},
	{'dt': 1636102800, 'main': {'temp': 41.58, 'feels_like': 36.37, 'temp_min': 41.58, 'temp_max': 41.58, 'pressure': 1019, 'sea_level': 1019, 'grnd_level': 988, 'humidity': 72, 'temp_kf': 0}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'clouds': {'all': 6}, 'wind': {'speed': 8.25, 'deg': 185, 'gust': 26.73}, 'visibility': 10000, 'pop': 0, 'sys': {'pod': 'n'}, 'dt_txt': '2021-11-05 09:00:00'},
	{'dt': 1636113600, 'main': {'temp': 60.68, 'feels_like': 34.84, 'temp_min': 40.68, 'temp_max': 40.68, 'pressure': 1019, 'sea_level': 1019, 'grnd_level': 988, 'humidity': 73, 'temp_kf': 0}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'clouds': {'all': 3}, 'wind': {'speed': 9.17, 'deg': 179, 'gust': 29.46}, 'visibility': 10000, 'pop': 0, 'sys': {'pod': 'n'}, 'dt_txt': '2021-11-05 12:00:00'},
	{'dt': 1636124400, 'main': {'temp': 64.2, 'feels_like': 38.46, 'temp_min': 44.2, 'temp_max': 44.2, 'pressure': 1019, 'sea_level': 1019, 'grnd_level': 988, 'humidity': 65, 'temp_kf': 0}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'clouds': {'all': 1}, 'wind': {'speed': 11.03, 'deg': 179, 'gust': 31.68}, 'visibility': 10000, 'pop': 0, 'sys': {'pod': 'd'}, 'dt_txt': '2021-11-05 15:00:00'},
	{'dt': 1636135200, 'main': {'temp': 64.14, 'feels_like': 51.46, 'temp_min': 54.14, 'temp_max': 54.14, 'pressure': 1015, 'sea_level': 1015, 'grnd_level': 985, 'humidity': 47, 'temp_kf': 0}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02d'}], 'clouds': {'all': 20}, 'wind': {'speed': 13.29, 'deg': 185, 'gust': 28.03}, 'visibility': 10000, 'pop': 0, 'sys': {'pod': 'd'}, 'dt_txt': '2021-11-05 18:00:00'},
	{'dt': 1636146000, 'main': {'temp': 64.63, 'feels_like': 51.91, 'temp_min': 54.63, 'temp_max': 54.63, 'pressure': 1013, 'sea_level': 1013, 'grnd_level': 983, 'humidity': 45, 'temp_kf': 0}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04d'}], 'clouds': {'all': 100}, 'wind': {'speed': 13.91, 'deg': 178, 'gust': 29.73}, 'visibility': 10000, 'pop': 0, 'sys': {'pod': 'd'}, 'dt_txt': '2021-11-05 21:00:00'},
	# Nov 6, 2021
	{'dt': 1636178400, 'main': {'temp': 47.57, 'feels_like': 42.76, 'temp_min': 47.57, 'temp_max': 47.57, 'pressure': 1014, 'sea_level': 1014, 'grnd_level': 983, 'humidity': 69, 'temp_kf': 0}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}], 'clouds': {'all': 69}, 'wind': {'speed': 10.74, 'deg': 198, 'gust': 28.95}, 'visibility': 10000, 'pop': 0, 'sys': {'pod': 'n'}, 'dt_txt': '2021-11-06 06:00:00'},
	{'dt': 1636189200, 'main': {'temp': 45.54, 'feels_like': 41.41, 'temp_min': 45.54, 'temp_max': 45.54, 'pressure': 1014, 'sea_level': 1014, 'grnd_level': 983, 'humidity': 81, 'temp_kf': 0}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'clouds': {'all': 0}, 'wind': {'speed': 7.81, 'deg': 199, 'gust': 21.14}, 'visibility': 10000, 'pop': 0, 'sys': {'pod': 'n'}, 'dt_txt': '2021-11-06 09:00:00'},
	{'dt': 1636200000, 'main': {'temp': 43.79, 'feels_like': 40.32, 'temp_min': 43.79, 'temp_max': 43.79, 'pressure': 1015, 'sea_level': 1015, 'grnd_level': 984, 'humidity': 89, 'temp_kf': 0}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'clouds': {'all': 1}, 'wind': {'speed': 5.93, 'deg': 207, 'gust': 17.76}, 'visibility': 10000, 'pop': 0, 'sys': {'pod': 'n'}, 'dt_txt': '2021-11-06 12:00:00'},
	{'dt': 1636210800, 'main': {'temp': 47.98, 'feels_like': 45.3, 'temp_min': 47.98, 'temp_max': 47.98, 'pressure': 1016, 'sea_level': 1016, 'grnd_level': 985, 'humidity': 73, 'temp_kf': 0}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02d'}], 'clouds': {'all': 24}, 'wind': {'speed': 5.93, 'deg': 210, 'gust': 16.06}, 'visibility': 10000, 'pop': 0, 'sys': {'pod': 'd'}, 'dt_txt': '2021-11-06 15:00:00'},
	{'dt': 1636221600, 'main': {'temp': 59.25, 'feels_like': 56.95, 'temp_min': 59.25, 'temp_max': 59.25, 'pressure': 1013, 'sea_level': 1013, 'grnd_level': 983, 'humidity': 44, 'temp_kf': 0}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03d'}], 'clouds': {'all': 42}, 'wind': {'speed': 5.99, 'deg': 191, 'gust': 10.63}, 'visibility': 10000, 'pop': 0, 'sys': {'pod': 'd'}, 'dt_txt': '2021-11-06 18:00:00'}]


expected_mapping_result = [
	# Nov 2, 2021
	Weather(temp=64.07, condition='Clouds', dt=datetime(2021, 11, 2, 6)),
	Weather(temp=62.38, condition='Drizzle', dt=datetime(2021, 11, 2, 9)),
	Weather(temp=61.44, condition='Clear', dt=datetime(2021, 11, 2, 12)),
	Weather(temp=64.5, condition='Rain', dt=datetime(2021, 11, 2, 15)),
	Weather(temp=60.48, condition='Clouds', dt=datetime(2021, 11, 2, 18)),
	Weather(temp=62.31, condition='Clouds', dt=datetime(2021, 11, 2, 21)),
	# Nov 3, 2021
	Weather(temp=34.84, condition='Clear', dt=datetime(2021, 11, 3, 6)),
	Weather(temp=83.71, condition='Clear', dt=datetime(2021, 11, 3, 9)),
	Weather(temp=82.86, condition='Clear', dt=datetime(2021, 11, 3, 12)),
	Weather(temp=76.19, condition='Clouds', dt=datetime(2021, 11, 3, 15)),
	Weather(temp=81.4, condition='Clouds', dt=datetime(2021, 11, 3, 18)),
	Weather(temp=44.26, condition='Clouds', dt=datetime(2021, 11, 3, 21)),
	# Nov 4, 2021
	Weather(temp=37.18, condition='Clouds', dt=datetime(2021, 11, 4, 6)),
	Weather(temp=76.23, condition='Clouds', dt=datetime(2021, 11, 4, 9)),
	Weather(temp=75.62, condition='Clouds', dt=datetime(2021, 11, 4, 12)),
	Weather(temp=69.97, condition='Clear', dt=datetime(2021, 11, 4, 15)),
	Weather(temp=78.7, condition='Clear', dt=datetime(2021, 11, 4, 18)),
	Weather(temp=52.0, condition='Clear', dt=datetime(2021, 11, 4, 21)),
	# Nov 5, 2021
	Weather(temp=43.0, condition='Clear', dt=datetime(2021, 11, 5, 6)),
	Weather(temp=41.58, condition='Clear', dt=datetime(2021, 11, 5, 9)),
	Weather(temp=60.68, condition='Clear', dt=datetime(2021, 11, 5, 12)),
	Weather(temp=64.2, condition='Clear', dt=datetime(2021, 11, 5, 15)),
	Weather(temp=64.14, condition='Clouds', dt=datetime(2021, 11, 5, 18)),
	Weather(temp=64.63, condition='Clouds', dt=datetime(2021, 11, 5, 21)),
	# Nov 6, 2021
	Weather(temp=47.57, condition='Clouds', dt=datetime(2021, 11, 6, 6)),
	Weather(temp=45.54, condition='Clear', dt=datetime(2021, 11, 6, 9)),
	Weather(temp=43.79, condition='Clear', dt=datetime(2021, 11, 6, 12)),
	Weather(temp=47.98, condition='Clouds', dt=datetime(2021, 11, 6, 15)),
	Weather(temp=59.25, condition='Clouds', dt=datetime(2021, 11, 6, 18))]

expected_filtering_result = [
	# Nov 2, 2021; Will get CALL. 1st and 3rd will be CALL and others will be EMAIL, but CALL came
	# first, so it breaks the tie
	Weather(temp=62.38, condition='Drizzle', dt=datetime(2021, 11, 2, 9)),
	Weather(temp=61.44, condition='Clear', dt=datetime(2021, 11, 2, 12)),
	Weather(temp=64.5, condition='Rain', dt=datetime(2021, 11, 2, 15)),
	Weather(temp=60.48, condition='Clouds', dt=datetime(2021, 11, 2, 18)),
	# Nov 3, 2021; Will get SMS
	Weather(temp=83.71, condition='Clear', dt=datetime(2021, 11, 3, 9)),
	Weather(temp=82.86, condition='Clear', dt=datetime(2021, 11, 3, 12)),
	Weather(temp=76.19, condition='Clouds', dt=datetime(2021, 11, 3, 15)),
	Weather(temp=81.4, condition='Clouds', dt=datetime(2021, 11, 3, 18)),
	# Nov 4, 2021; Will get EMAIL by default, since not enough completely meet SMS requirements
	# of 75+ AND Clear
	Weather(temp=76.23, condition='Clouds', dt=datetime(2021, 11, 4, 9)), # default EMAIL
	Weather(temp=75.62, condition='Clouds', dt=datetime(2021, 11, 4, 12)), # default EMAIL
	Weather(temp=69.97, condition='Clear', dt=datetime(2021, 11, 4, 15)), # EMAIL
	Weather(temp=78.7, condition='Clear', dt=datetime(2021, 11, 4, 18)), # SMS
	# Nov 5, 2021; Will get EMAIL, since more than half are in that range
	Weather(temp=41.58, condition='Clear', dt=datetime(2021, 11, 5, 9)),
	Weather(temp=60.68, condition='Clear', dt=datetime(2021, 11, 5, 12)),
	Weather(temp=64.2, condition='Clear', dt=datetime(2021, 11, 5, 15)),
	Weather(temp=64.14, condition='Clouds', dt=datetime(2021, 11, 5, 18)),
	# Nov 6, 2021; Will get CALL, for low temperatures
	Weather(temp=45.54, condition='Clear', dt=datetime(2021, 11, 6, 9)),
	Weather(temp=43.79, condition='Clear', dt=datetime(2021, 11, 6, 12)),
	Weather(temp=47.98, condition='Clouds', dt=datetime(2021, 11, 6, 15)),
	Weather(temp=59.25, condition='Clouds', dt=datetime(2021, 11, 6, 18))]


expected_final_result = {
	date(2021, 11, 2): MessageType.CALL,
	date(2021, 11, 3): MessageType.SMS,
	date(2021, 11, 4): MessageType.EMAIL,
	date(2021, 11, 5): MessageType.EMAIL,
	date(2021, 11, 6): MessageType.CALL}

expected_final_result_SMS_default = {
	date(2021, 11, 2): MessageType.CALL,
	date(2021, 11, 3): MessageType.SMS,
	date(2021, 11, 4): MessageType.SMS,
	date(2021, 11, 5): MessageType.EMAIL,
	date(2021, 11, 6): MessageType.CALL}


class WeatherTest(TestCase):
	def test_mapping(self):
		result = map_json_list_to_weather(data)
		self.assertEqual(list(result), expected_mapping_result)

	def test_filtering(self):
		# The first and last entries each day are filtered out
		result = filter_irrelevant_times(expected_mapping_result)
		self.assertEqual(list(result), expected_filtering_result)

	def test_calculation(self):
		result = get_messaging_forecast(data)
		self.assertEqual(result, expected_final_result)

	def test_calculator_with_alt_default(self):
		Weather.DEFAULT_MESSAGE_TYPE = MessageType.SMS
		result = get_messaging_forecast(data)
		self.assertEqual(result, expected_final_result_SMS_default)
		Weather.DEFAULT_MESSAGE_TYPE = None  # Setting it to None causes it to look up the default in the config again