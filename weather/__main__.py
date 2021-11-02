from itertools import groupby

from weather.openweather import get_default_data
from weather.weather_service import get_messaging_forecast

def main():
    data = get_default_data()
    if data['cod'] != '200':
        raise Exception(data['message'])
    weather_data = get_messaging_forecast(data['list'])
    print()
    print('Message type suggestions based on weather (5-day forecast):')
    for date, msg_type in weather_data.items():
        print()
        print(date.strftime('%b %d, %Y:'))
        print(f'\t{msg_type.name}')


if __name__ == '__main__':
    main()

