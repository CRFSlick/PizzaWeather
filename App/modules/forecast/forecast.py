import os
import time
import json
import requests


class Forecast(object):

    min_days = 0
    max_days = 40
    one_week = 7

    def __init__(self, api_key, lat, lon, days):
        """
        Creates Forecast object

        Args:
            api_key (str): OpenWeather.com api key
            lat (float): lat
            lon (float): lon
        """

        self.api_key = api_key
        self._url_icon = {'head': 'http://openweathermap.org/img/wn/', 'tail': '@2x.png'}
        self.lat = lat
        self.lon = lon
        self.days = days
        self._data = None
        self._country_code = None

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

    @property
    def url_icon(self):
        """
        Returns:
            url_icon (str)
        """
        return self._url_icon

    @property
    def country_code(self):
        """
        Returns:
            country_code (str)
        """
        return self._country_code

    @property
    def days(self):
        """
        Returns:
            days (list)
        """
        return self._days

    @days.setter
    def days(self, value):
        """
        Sets days to be returned

        Args:
            value (int) OR (list)

        Raises:
            ValueError: if value is not of type (int) or (list)
        """
        if value is not None:
            value = self.__validate_data(value, 'days', [int, list])
            if isinstance(value, int):
                if self.min_days <= value <= self.max_days:
                    days_array = []
                    for x in range(self.min_days, value):
                        days_array.append(x)
                    self._days = days_array
                else:
                    raise ValueError(f'days value must be between 0 and 40, got {value}')
            elif isinstance(value, list):
                self._days = value
        else:
            days_array = []
            for x in range(self.min_days, self.one_week):
                days_array.append(x)
            self._days = days_array

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
        return 'http://api.openweathermap.org/data/2.5/forecast'

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
            if data['cod'] == '200':
                weather_dict = {}
                for x in self.days:
                    dt = data['list'][x]['dt']
                    overview = data['list'][x]['weather'][0]['main']
                    description = data['list'][x]['weather'][0]['description']
                    icon_url = self.url_icon['head'] + data['list'][x]['weather'][0]['icon'] + self.url_icon['tail']
                    weather_dict[x] = [dt, [overview, description, icon_url]]
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
            if data['cod'] == '200':
                temperature_dict = {}
                for x in self.days:
                    dt = data['list'][x]['dt']
                    temp = data['list'][x]['main']['temp']
                    temp_min = data['list'][x]['main']['temp_min']
                    temp_max = data['list'][x]['main']['temp_max']
                    temperature_dict[x] = [dt, [temp, temp_min, temp_max]]
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
            if data['cod'] == '200':
                humidity_dict = {}
                for x in self.days:
                    dt = data['list'][x]['dt']
                    humidity = data['list'][x]['main']['humidity']
                    humidity_dict[x] = [dt, humidity]
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
            if data['cod'] == '200':
                wind_dict = {}
                for x in self.days:
                    dt = data['list'][x]['dt']
                    wind = data['list'][x]['wind']['speed']
                    degrees = data['list'][x]['wind']['deg']
                    wind_dict[x] = [dt, [wind, degrees]]
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
            if data['cod'] == '200':
                cloud_dict = {}
                for x in self.days:
                    dt = data['list'][x]['dt']
                    cloud_cover = data['list'][x]['clouds']['all']
                    cloud_dict[x] = [dt, cloud_cover]
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
            if data['cod'] == '200':
                rain_dict = {}
                for x in self.days:
                    dt = data['list'][x]['dt']
                    try:
                        precipitation = data['list'][x]['rain']['3h']
                    except KeyError:
                        precipitation = 0
                    rain_dict[x] = [dt, precipitation]
                return rain_dict
            else:
                raise Exception(f'API error! | Response Code: {data["cod"]} | Message: {data["message"]}')
        else:
            raise Exception(f'you must first fetch data from the API using method fetch_forecast() before requesting '
                            f'precipitation information')
