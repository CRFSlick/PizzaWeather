from App.modules.forecast.forecast import Forecast
from App.modules.current.current import Current
from App.modules.UV_Index.UV_Index import UVI
from App.modules.log.log import Log
# import zipcodes
import math


class API(object):

    def __init__(self, api_key, lat, lon, days):

        self.api_key = api_key
        self.lat = float(lat)
        self.lon = float(lon)

        self.current_obj = Current(api_key=self.api_key, lat=self.lat, lon=self.lon)
        self.current_obj.fetch_forecast()

        self.forecast_obj = Forecast(api_key=self.api_key, lat=self.lat, lon=self.lon, days=days)
        self.forecast_obj.fetch_forecast()

        self.uv_obj = UVI(api_key=api_key, lat=self.lat, lon=self.lon, cnt=1)
        # self.radar_obj = Base(api_key=api_key, city='Something, since apparently this is required but never used...')

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
        self._api_key = value
        
    @property
    def zip_code(self):
        """
        Returns:
            zip_code (str)
        """
        return self._zip_code

    @zip_code.setter
    def zip_code(self, value):
        """
        Returns:
            zip_code (str)
        """
        self._zip_code = value

    @property
    def city(self):
        """
        Returns:
            city (str)
        """
        return self._city

    @city.setter
    def city(self, value):
        """
        Returns:
            city (str)
        """
        self._city = value

    @property
    def country(self):
        """
        Returns:
            country (str)
        """
        return self._country

    @country.setter
    def country(self, value):
        """
        Returns:
            country (str)
        """
        self._country = value

    @property
    def lat(self):
        """
        Returns:
            lat (str)
        """

        return self._lat

    @lat.setter
    def lat(self, value):
        """
        Returns:
            lat (str)
        """
        self._lat = value

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
        Returns:
            lon (str)
        """
        self._lon = value

    @property
    def _current_obj(self):
        """
        Returns:
            api_key (str)
        """
        if self.current_obj:
            return self.current_obj
        else:
            raise ValueError("you must instantiate the 'Current' class first!")

    @property
    def _forecast_obj(self):
        """
        Returns:
            api_key (str)
        """
        if self.forecast_obj:
            return self.forecast_obj
        else:
            raise ValueError("you must instantiate the 'Forecast' class first!")

    @property
    def _uv_obj(self):
        """
        Returns:
            api_key (str)
        """
        if self.uv_obj:
            return self.uv_obj
        else:
            raise ValueError("you must instantiate the 'UV' class first!")

    # @property
    # def _radar_obj(self):
    #     """
    #     Returns:
    #         api_key (str)
    #     """
    #     if self.radar_obj:
    #         return self.radar_obj
    #     else:
    #         raise ValueError("you must instantiate the 'Radar' class first!")

    @property
    def current_sunrise(self):
        """
        Gets current prediction of local sunrise time

        Returns:
            main (dict)
        """
        main = {}
        data = self._current_obj.sunrise()
        for day in data:
            main[day] = {'datetime': data[day][0], 'sunrise': data[day][1]}
        return main

    @property
    def current_sunset(self):
        """
        Gets current prediction of local sunset time

        Returns:
            main (dict)
        """
        main = {}
        data = self._current_obj.sunset()
        for day in data:
            main[day] = {'datetime': data[day][0], 'sunset': data[day][1]}
        return main

    @property
    def current_timezone_offset(self):
        """
        Gets timezone offset for displaying

        Returns:
            main (dict)
        """
        main = {}
        data = self._current_obj.timezone_offset()
        for day in data:
            main[day] = {'datetime': data[day][0], 'timezone_offset': data[day][1]}
        return main

    @property
    def current_weather(self):
        """
        Gets current weather forecast

        Returns:
            main (dict)
        """
        main = {}
        data = self._current_obj.weather()
        for day in data:
            main[day] = {'datetime': data[day][0], 'weather': data[day][1][0]}
        return main

    @property
    def current_weather_description(self):
        """
        Gets current weather forecast description

        Returns:
            main (dict)
        """
        main = {}
        data = self._current_obj.weather()
        for day in data:
            main[day] = {'datetime': data[day][0], 'weather-description': data[day][1][1]}
        return main

    @property
    def current_weather_icon_url(self):
        """
        Gets URL for weather icon

        Returns:
            main (dict)
        """
        main = {}
        data = self._current_obj.weather()
        for day in data:
            main[day] = {'datetime': data[day][0], 'weather-icon-url': data[day][1][2]}
        return main

    @property
    def current_temperature_average(self):
        """
        Gets current temperature average

        Returns:
            main (dict)
        """
        main = {}
        data = self._current_obj.temperature()
        for day in data:
            dt = data[day][0]
            kelvin = round(data[day][1][0], 2)
            celsius = round(self.kelvin_to_celsius(kelvin), 2)
            fahrenheit = round(self.kelvin_to_fahrenheit(kelvin), 2)
            main[day] = {'datetime': dt, 'celsius': f'{celsius}', 'fahrenheit':
                f'{fahrenheit}', 'kelvin':f'{kelvin}'}
        return main

    @property
    def current_temperature_min(self):
        """
        Gets current temperature min

        Returns:
            main (dict)
        """
        main = {}
        data = self._current_obj.temperature()
        for day in data:
            dt = data[day][0]
            kelvin = round(data[day][1][1], 2)
            celsius = round(self.kelvin_to_celsius(kelvin), 2)
            fahrenheit = round(self.kelvin_to_fahrenheit(kelvin), 2)
            main[day] = {'datetime': dt, 'celsius': f'{celsius}', 'fahrenheit':
                f'{fahrenheit}', 'kelvin': f'{kelvin}'}
        return main

    @property
    def current_temperature_max(self):
        """
        Gets current temperature max

        Returns:
            main (dict)
        """
        main = {}
        data = self._current_obj.temperature()
        for day in data:
            dt = data[day][0]
            kelvin = round(data[day][1][2], 2)
            celsius = round(self.kelvin_to_celsius(kelvin), 2)
            fahrenheit = round(self.kelvin_to_fahrenheit(kelvin), 2)
            main[day] = {'datetime': dt, 'celsius': f'{celsius}', 'fahrenheit':
                f'{fahrenheit}', 'kelvin': f'{kelvin}'}
        return main

    @property
    def current_humidity(self):
        """
        Gets current humidity

        Returns:
            main (dict)
        """
        main = {}
        data = self._current_obj.humidity()
        for day in data:
            main[day] = {'datetime': data[day][0], 'humidity': data[day][1]}
        return main

    @property
    def current_wind_speed(self):
        """
        Gets current wind speed

        Returns:
            main (dict)
        """
        main = {}
        data = self._current_obj.wind()
        for day in data:
            main[day] = {'datetime': data[day][0], 'wind-speed': data[day][1][0]}
        return main

    @property
    def current_wind_direction(self):
        """
        Gets current wind direction

        Returns:
            main (dict)
        """
        main = {}
        data = self._current_obj.wind()
        for day in data:
            main[day] = {'datetime': data[day][0], 'wind-direction': data[day][1][1]}
        return main

    @property
    def current_cloud_cover(self):
        """
        Gets current cloud cover

        Returns:
            main (dict)
        """
        main = {}
        data = self._current_obj.cloud_cover()
        for day in data:
            main[day] = {'datetime': data[day][0], 'cloud-cover': data[day][1]}
        return main

    @property
    def current_precipitation(self):
        """
        Gets current precipitation

        Returns:
            main (dict)
        """
        main = {}
        data = self._current_obj.precipitation()
        for day in data:
            main[day] = {'datetime': data[day][0], 'precipitation': data[day][1]}
        return main

    @property
    def uv_index_today(self):
        """
        Gets current UV index

        Returns:
            main (dict)
        """
        main = {}
        data = self._uv_obj.get_json()
        for i in data:
            main[0] = {'datetime': data[0]['date'], 'uv-index': data[0]['value']}
            return main
        return None

    @staticmethod
    def convert_to_tile(latitude, longitude, zoom):
        """
        Converts lat lon to tile for API use

        Args:
            latitude (int)
            longitude (int)
            zoom (int)

        Returns:
            tiles (tuple)
        """
        lat_rad = math.radians(latitude)
        n = 2.0 ** zoom
        xtile = int((longitude + 180.0) / 360.0 * n)
        ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
        tiles = (xtile, ytile)
        return tiles

    def get_radar_urls(self):
        """
        Gets radar URLs

        Args:
            None

        Returns:
            urls (dict)
        """
        zoom = 8
        urls = {}
        layers = {'precipitation': 'precipitation_new',
                  'temperature': 'temp_new',
                  'pressure': 'pressure_new',
                  'clouds': 'clouds_new',
                  'wind': 'wind_new'}

        tiles = self.convert_to_tile(self.lat, self.lon, zoom)
        x_tile = tiles[0]
        y_tile = tiles[1]

        urls['base'] = f'http://sat.owm.io/sql/{zoom}/{x_tile}/{y_tile}?from=s2&appid={self.api_key}'

        for key in layers:
            urls[key] = f'https://tile.openweathermap.org/map/{layers[key]}/{zoom}/{x_tile}/{y_tile}.png?' \
                f'appid={self.api_key}'

        return urls

    @staticmethod
    def kelvin_to_celsius(kelvin):
        return kelvin - 273.15

    @staticmethod
    def kelvin_to_fahrenheit(kelvin):
        return (kelvin - 273.15) * 9/5 + 32
