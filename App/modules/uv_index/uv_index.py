import json
import requests


class UVI(object):
    _api_key = None
    _lat = None
    _lon = None
    _cnt = None

    def __init__(self, api_key, lat, lon, cnt=None):

        self.api_key = api_key
        self.lat = lat
        self.lon = lon
        self.cnt = cnt

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
        Returns:
            api_key (str)
        """
        self._api_key = str(value)

    @property
    def lat(self):
        """
        Returns:
            lat (float)
        """
        return self._lat

    @lat.setter
    def lat(self, value):
        """
        Returns:
            lat (float)
        """
        self._lat = float(value)

    @property
    def lon(self):
        """
        Returns:
            lon (float)
        """
        return self._lon

    @lon.setter
    def lon(self, value):
        """
        Returns:
            lon (float)
        """
        self._lon = float(value)

    @property
    def cnt(self):
        """
        Returns:
            cnt (float)
        """
        return self._cnt

    @cnt.setter
    def cnt(self, value):
        """
        Returns:
            cnt (float)
        """
        self._cnt = float(value)

    @property
    def __base_url(self):
        """
        Returns:
            base_url (str)
        """
        return "http://api.openweathermap.org/data/2.5/uvi/forecast"

    @property
    def __params(self):
        """
        Returns:
            params (dict)
        """
        return {'api_key': {self.api_key}, 'lat': {self.lat}, 'lon': {self.lon}}

    @staticmethod
    def __validate_float(input, name, float):
        """
        Validates an argument to be a float

        Args:
            input (float/list)
            name (str)
            float (object)

        Returns:
            input (float/list)

        Raises:
            ValueError
        """
        if isinstance(float, list):
            if input == float:
                return input
            raise ValueError(f"expected '{name}' to be a floating point value, but got '{input}' instead.")
        else:
            if input == float:
                return input
            raise ValueError(f"expected '{name}' to be a floating point value, but got '{input}' instead.")

    @staticmethod
    def __validate_string(input, name, str):
        """
        Validates an argument to be a str

        Args:
            input (str/list)
            name (str)
            str (object)

        Returns:
            input (str/list)

        Raises:
            ValueError
        """
        if isinstance(str, list):
            if input == str:
                return input
            raise ValueError(f"expected '{name}' to be a string value, but got '{input}' instead.")
        else:
            if input == str:
                return input
            raise ValueError(f"expected '{name}' to be a string value, but got '{input}' instead.")

    def __get_UV_Index(self):
        """
        Gets UV index data

        Returns:
            response (dict)

        Raises:
            Exception
        """
        response = json.loads(requests.get(url=self.__base_url, params=self.__params).text)
        if response.cod == '200':
            return response
        else:
            raise Exception(f'{response.cod}: {response.message}')

    def get_json(self):
        """
        Returns:
            uvi (dict)
        """
        uvi = self.__get_UV_Index()
        return uvi
