from App.modules.forecast.forecast import Forecast
from App import app

api_key = app.config['OPENWEATHERMAP_API_KEY']
# city = 'Chicago'
# country = 'United States of America'
lat = 42.0584
lon = -87.9836

forecast = Forecast(api_key=api_key, lat=lat, lon=lon, days=40)
forecast.fetch_forecast()
print(forecast.weather())
print(forecast.temperature())
print(forecast.humidity())
print(forecast.wind())
print(forecast.cloud_cover())
print(forecast.precipitation())

print()

forecast.city = 'Manhattan'
forecast.days = 3
forecast.fetch_forecast()
print(forecast.weather())
print(forecast.temperature())
print(forecast.humidity())
print(forecast.wind())
print(forecast.cloud_cover())
print(forecast.precipitation())

print()

forecast.city = 'New York'
forecast.days = [2, 5, 9]
forecast.fetch_forecast()
print(forecast.weather())
print(forecast.temperature())
print(forecast.humidity())
print(forecast.wind())
print(forecast.cloud_cover())
print(forecast.precipitation())
