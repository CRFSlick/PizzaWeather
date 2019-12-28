import unittest
from App.modules.forecast.forecast import Forecast
from App import app


class ForecastTestClass(unittest.TestCase):
    """Tests Forecast class"""

    def setUp(self):
        self.api_key = app.config['OPENWEATHERMAP_API_KEY']

    def test_constructor_api_key(self):
        forecast = Forecast(api_key=self.api_key, lat=0.0, lon=0.0, days=0)
        self.assertEqual(forecast.api_key, self.api_key, f"api_key constructor is not initializing to {self.api_key}")

    def test_constructor_lat(self):
        forecast = Forecast(api_key=self.api_key, lat=10.0, lon=0.0, days=0)
        self.assertEqual(forecast.lat, 10.0, "lat constructor is not initializing to 10.0!")

    def test_constructor_lon(self):
        forecast = Forecast(api_key=self.api_key, lat=0.0, lon=10.0, days=0)
        self.assertEqual(forecast.lon, 10.0, "lon constructor is not initializing to 10.0!")

    def test_constructor_days_method_one(self):
        forecast = Forecast(api_key=self.api_key, lat=0.0, lon=0.0, days=3)
        self.assertEqual(forecast.days, [0, 1, 2], "days constructor is not initializing to [0, 1, 2]!")

    def test_constructor_days_method_two(self):
        forecast = Forecast(api_key=self.api_key, lat=0.0, lon=0.0, days=[0, 3])
        self.assertEqual(forecast.days, [0, 3], "days constructor is not initializing to [0, 3]!")


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)