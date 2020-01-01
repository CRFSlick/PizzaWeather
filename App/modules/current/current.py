import os
import time
import json
import requests


class Current(object):

    min_days = 0
    max_days = 40
    one_week = 7

    def __init__(self, api_key, lat, lon):
        """
        Creates Forecast object

        Args:
            api_key (str): OpenWeather.com api key
            lat (str): lat
            lon (str): lon
        """

        self.api_key = api_key
        self._url_icon = {'head': 'http://openweathermap.org/img/wn/', 'tail': '@2x.png'}
        self.lat = lat
        self.lon = lon

    @property
    def api_key(self):
        """
        Returns:
            api_key (str)
        """
        return self._api_key

    @api_key.setter
    def api_key(self, value):
        """
        Sets api_key

        Args:
            value (str)

        Raises:
            ValueError: if value is not of type (str)
        """
        self._api_key = self.__validate_data(value, 'api_key', str)

    @property
    def url_icon(self):
        """
        Returns:
            url_icon (str)
        """
        return self._url_icon

    @property
    def lat(self):
        """
        Returns:
            lat
        """
        return self._lat

    @lat.setter
    def lat(self, value):
        """
        Sets lat

        Args:
            value (str)

        Raises:
            ValueError: if value is not of type (str)
        """
        self._lat = self.__validate_data(value, 'lat', float)

    @property
    def lon(self):
        """
        Returns:
            lon (str)
        """
        return self._lon

    @lon.setter
    def lon(self, value):
        """
        Sets lon

        Args:
            value (str)

        Raises:
            ValueError: if value is not of type (str)
        """
        self._lon = self.__validate_data(value, 'lon', float)
        self._country_code = None

    @property
    def country_code(self):
        """
        Returns:
            country_code (str)
        """
        return self._country_code

    @property
    def __params(self):
        """
        Returns:
            params (dict)
        """
        return {'lat': self.lat, 'lon': self.lon, 'APPID': self.api_key}

    @property
    def __base_url(self):
        """
        Returns:
            base_url (str)
        """
        return 'http://api.openweathermap.org/data/2.5/weather'

    @property
    def request(self):
        """
        Returns:
            request URL for debug purposes
        """
        url = f'{self.__base_url}?'
        for key in self.__params:
            url += f'{key}={self.__params[key]}&'
        return url.strip('&').replace(' ', '%20')

    @property
    def data(self):
        """
        Returns:
            data (list)
        """
        return self._data

    @staticmethod
    def __validate_data(data, name, data_type):
        """
        Validates data

        Args:
            data (any): data to be validated
            name (str): name of data
            data_type (class type): type of data that is required
        """
        if isinstance(data_type, list):
            for x in data_type:
                if type(data) == x:
                    return data
            raise ValueError(f"expected '{name}' to be of type {data_type}, but got {type(data)}!")
        else:
            if type(data) == data_type:
                return data
            raise ValueError(f"expected '{name}' to be of type {data_type}, but got {type(data)}!")

    @staticmethod
    def __get_country_code(country):
        """
        Gets country code given country

        Args:
            country (str)

        Returns:
            country_code (str)
        """
        try:
            current_path = os.path.dirname(__file__)
            if '\\' in current_path:
                slash = '\\'
            elif '/' in current_path:
                slash = '/'
            else:
                slash = '/'
            filename = f'{slash}resources{slash}json{slash}ISO_3116.json'
            file_path = os.path.dirname(__file__)[0:os.path.dirname(__file__).find(f'{slash}App{slash}') +
                                                    len(f'{slash}App{slash}')] + filename
            if os.path.exists(file_path):
                with open(file_path, 'r') as ISO_3166:
                    iso_3116 = json.loads(ISO_3166.read())
                    ISO_3166.close()
            else:
                raise FileNotFoundError
        except FileNotFoundError:
            raise FileNotFoundError('could not find critical file \"ISO_3116.json\"')

        if len(country) == 2:
            for country_info in iso_3116:
                if country_info['iso_3166-2'].split(':')[1] == country.upper():
                    return country_info['iso_3166-2'].split(':')[1]

        for country_info in iso_3116:
            if country_info['name'].lower() == country.lower():
                return country_info['iso_3166-2'].split(':')[1]

        raise ValueError(f'could not find ISO_3116 country code for country "{country}", please enter a valid country '
                         f'name or country code')

    def fetch_forecast(self):
        """
        Fetches JSON forecast data

        Args:
            None

        Returns:
            JSON Weather Data
        """
        time.sleep(1.1)
        self._data = json.loads(requests.get(url=self.__base_url, params=self.__params).text)

    def weather(self):
        """
        Puts together weather descriptions

        Args:
            None

        Reruns:
            weather_dict
        """
        data = self.data
        if data:
            if data['cod'] == 200:
                weather_dict = {}
                dt = data['dt']
                overview = data['weather'][0]['main']
                description = data['weather'][0]['description']
                icon_url = self.url_icon['head'] + data['weather'][0]['icon'] + self.url_icon['tail']
                weather_dict[0] = [dt, [overview, description, icon_url]]
                return weather_dict
            else:
                raise Exception(f'API error! | Response Code: {data["cod"]} | Message: {data["message"]}')
        else:
            raise Exception(f'you must first fetch data from the API using method fetch_forecast() before requesting '
                            f'weather information')

    def temperature(self):
        """
        Puts together temperature forecast

        Args:
            None

        Reruns:
            temperature_dict
        """
        data = self.data
        if data:
            if data['cod'] == 200:
                temperature_dict = {}
                dt = data['dt']
                temp = data['main']['temp']
                temp_min = data['main']['temp_min']
                temp_max = data['main']['temp_max']
                temp_average = (temp_min + temp_max) / 2
                temperature_dict[0] = [dt, [temp, temp_min, temp_max, temp_average]]
                return temperature_dict
            else:
                raise Exception(f'API error! | Response Code: {data["cod"]} | Message: {data["message"]}')
        else:
            raise Exception(f'you must first fetch data from the API using method fetch_forecast() before requesting '
                            f'temperature information')

    def humidity(self):
        """
        Puts together humidity forecast

        Args:
            None

        Reruns:
            humidity_dict
        """
        data = self.data
        if data:
            if data['cod'] == 200:
                humidity_dict = {}
                dt = data['dt']
                humidity = data['main']['humidity']
                humidity_dict[0] = [dt, humidity]
                return humidity_dict
            else:
                raise Exception(f'API error! | Response Code: {data["cod"]} | Message: {data["message"]}')
        else:
            raise Exception(f'you must first fetch data from the API using method fetch_forecast() before requesting '
                            f'humidity information')

    def wind(self):
        """
        Puts together wind forecast

        Args:
            None

        Reruns:
            wind_dict
        """
        data = self.data
        if data:
            if data['cod'] == 200:
                wind_dict = {}
                dt = data['dt']
                wind = data['wind']['speed']
                try:
                    degrees = data['wind']['deg']
                    wind_dict[0] = [dt, [wind, degrees]]
                    return wind_dict
                except KeyError:
                    try:
                        gust = data['wind']['gust']
                        wind_dict[0] = [dt, [wind, gust]]
                        return wind_dict
                    except:
                        wind_dict[0] = [dt, [wind, 'Unknown']]
                        return wind_dict
            else:
                raise Exception(f'API error! | Response Code: {data["cod"]} | Message: {data["message"]}')
        else:
            raise Exception(f'you must first fetch data from the API using method fetch_forecast() before requesting '
                            f'wind information')

    def cloud_cover(self):
        """
        Puts together cloud cover forecast

        Args:
            None

        Reruns:
            cloud_dict
        """
        data = self.data
        if data:
            if data['cod'] == 200:
                cloud_dict = {}
                dt = data['dt']
                cloud_cover = data['clouds']['all']
                cloud_dict[0] = [dt, cloud_cover]
                return cloud_dict
            else:
                raise Exception(f'API error! | Response Code: {data["cod"]} | Message: {data["message"]}')
        else:
            raise Exception(f'you must first fetch data from the API using method fetch_forecast() before requesting '
                            f'cloud cover information')

    def precipitation(self):
        """
        Puts together precipitation forecast

        Args:
            None

        Reruns:
            precipitation_dict
        """
        data = self.data
        if data:
            if data['cod'] == 200:
                rain_dict = {}
                dt = data['dt']
                try:
                    precipitation = data['rain']['1h']
                except KeyError:
                    precipitation = 0
                rain_dict[0] = [dt, precipitation]
                return rain_dict
            else:
                raise Exception(f'API error! | Response Code: {data["cod"]} | Message: {data["message"]}')
        else:
            raise Exception(f'you must first fetch data from the API using method fetch_forecast() before requesting '
                            f'precipitation information')

    def sunrise(self):
        """
        Puts together sunrise datetime

        Args:
            None

        Reruns:
            weather_dict
        """
        data = self.data
        if data:
            if data['cod'] == 200:
                weather_dict = {}
                dt = data['dt']
                dt_sunrise = data['sys']['sunrise']
                weather_dict[0] = [dt, dt_sunrise]
                return weather_dict
            else:
                raise Exception(f'API error! | Response Code: {data["cod"]} | Message: {data["message"]}')
        else:
            raise Exception(f'you must first fetch data from the API using method fetch_forecast() before requesting '
                            f'weather information')

    def sunset(self):
        """
        Puts together sunset datetime

        Args:
            None

        Reruns:
            weather_dict
        """
        data = self.data
        if data:
            if data['cod'] == 200:
                weather_dict = {}
                dt = data['dt']
                dt_sunset = data['sys']['sunset']
                weather_dict[0] = [dt, dt_sunset]
                return weather_dict
            else:
                raise Exception(f'API error! | Response Code: {data["cod"]} | Message: {data["message"]}')
        else:
            raise Exception(f'you must first fetch data from the API using method fetch_forecast() before requesting '
                            f'weather information')

    def timezone_offset(self):
        """
        Puts together sunset datetime

        Args:
            None

        Reruns:
            weather_dict
        """
        data = self.data
        if data:
            if data['cod'] == 200:
                weather_dict = {}
                dt = data['dt']
                dt_offset = data['timezone']
                weather_dict[0] = [dt, dt_offset]
                return weather_dict
            else:
                raise Exception(f'API error! | Response Code: {data["cod"]} | Message: {data["message"]}')
        else:
            raise Exception(f'you must first fetch data from the API using method fetch_forecast() before requesting '
                            f'weather information')
