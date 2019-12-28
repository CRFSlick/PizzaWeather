#from App.modules.current.current import Current
from App.routes.routes import app
from current import Current
api_key = app.config['OPENWEATHERMAP_API_KEY']
# city = 'Chicago'
# country = 'United States of America'
lat = 42.0584
lon = -87.9836

# forecast = Current(api_key=api_key, city=city, country=country)
forecast = Current(api_key=api_key, lat=lat, lon=lon)
forecast.fetch_forecast()
print(forecast.weather())
print(forecast.temperature())
print(forecast.humidity())
print(forecast.wind())
print(forecast.cloud_cover())
print(forecast.precipitation())
print(forecast.sunrise())
print(forecast.sunset())

print()

forecast.city = 'Manhattan'
forecast.days = 2
forecast.fetch_forecast()
print(forecast.weather())
print(forecast.temperature())
print(forecast.humidity())
print(forecast.wind())
print(forecast.cloud_cover())
print(forecast.precipitation())
print(forecast.sunrise())
print(forecast.sunset())

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
print(forecast.sunrise())
print(forecast.sunset())
