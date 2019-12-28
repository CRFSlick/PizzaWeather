import json
import requests


class UVI(object):
    _appid = None
    _lat = None
    _lon = None
    _cnt = None

    def __init__(self, appid, lat, lon, cnt=None):

        self.appid = appid
        self.lat = lat
        self.lon = lon
        self.cnt = cnt

    @property
    def appid(self):
        return self._appid

    @appid.setter
    def appid(self, value):
        self._appid = str(value)

    @property
    def lat(self):
        return self._lat

    @lat.setter
    def lat(self, value):
        self._lat = float(value)

    @property
    def lon(self):
        return self._lon

    @lon.setter
    def lon(self, value):
        self._lon = float(value)

    @property
    def cnt(self):
        return self._cnt

    @cnt.setter
    def cnt(self, value):
        self._cnt = float(value)

    @property
    def __base_url(self):
        return "http://api.openweathermap.org/data/2.5/uvi/forecast"

    @property
    def __params(self):
        return {'appid':{self.appid}, 'lat':{self.lat}, 'lon':{self.lon}}

    @property
    def requests(self):
        url = f'{self.__base_url}?'
        for key in self.__params:
            url += f'{key}{self.__params[key]}'
        return url

    @staticmethod
    def __validate_float(input, name, float):
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
        if isinstance(str, list):
            if input == str:
                return input
            raise ValueError(f"expected '{name}' to be a string value, but got '{input}' instead.")
        else:
            if input == str:
                return input
            raise ValueError(f"expected '{name}' to be a string value, but got '{input}' instead.")

    def __get_UV_Index(self):
        return json.loads(requests.get(url=self.__base_url,
                          params=self.__params).text)

    def get_json(self):
        uvi = self.__get_UV_Index()
        return uvi
