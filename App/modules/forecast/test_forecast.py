"""
Sources:
    https://stackoverflow.com/questions/2648329/python-unit-test-how-to-add-some-sleeping-time-between-test-cases
"""

import time
import unittest
from App.modules.forecast.forecast import Forecast
from App import app


class ForecastTestClass(unittest.TestCase):
    """Tests Forecast class"""

    def setUp(self):
        self.api_key = app.config['OPENWEATHERMAP_API_KEY']

    # def tearDown(self):
    #     time.sleep(1.1)  # sleep time in seconds

    def test_constructor_api_key(self):
        forecast = Forecast(api_key=self.api_key, lat='0', lon='0', days=0)
        self.assertEqual(forecast.api_key, self.api_key, f"api_key constructor is not initializing to {self.api_key}")

    def test_constructor_city(self):
        forecast = Forecast(api_key=self.api_key, city='Chicago', country='US')
        self.assertEqual(forecast.city, 'Chicago', "city constructor is not initializing to \'Chicago\'")

    def test_constructor_country(self):
        forecast = Forecast(api_key=self.api_key, city='Chicago', country='US')
        self.assertEqual(forecast.country, 'US', "city constructor is not initializing to \'US\'")

    def test_constructor_country_code(self):
        forecast = Forecast(api_key=self.api_key, city='Chicago', country='Canada')
        self.assertEqual(forecast.country_code, 'CA', "country code constructor is not initializing \'Canada\' to "
                                                      "\'CA\'")

    def test_constructor_days_list(self):
        forecast = Forecast(api_key=self.api_key, city='Chicago', country='US', days=[10, 11])
        self.assertEqual(forecast.days, [10, 11], "days constructor is not initializing to [10, 11]")

    def test_constructor_days_int(self):
        forecast = Forecast(api_key=self.api_key, city='Chicago', country='US', days=3)
        self.assertEqual(forecast.days, [0, 1, 2], "days constructor is not initializing 3 to range array of [0, 1, 2]")

    def test_api_key_with_bad_value_abc123(self):
        forecast = Forecast(api_key='abc123', city='Chicago', country='US')
        self.assertRaises(Exception, forecast.weather)

    def test_city_with_bad_value_abc123(self):
        forecast = Forecast(api_key=self.api_key, city='abc123', country='US')
        self.assertRaises(Exception, forecast.weather)


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)