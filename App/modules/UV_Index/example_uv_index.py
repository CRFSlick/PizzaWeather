from App.modules.UV_Index.UV_Index import UVI as UV_Index_Module
from App import app

# The latitude and longitude example from openweathermap.org
appid = app.config['OPENWEATHERMAP_API_KEY']
lat = 37.75
lon = -122.37
cnt = 1

UV_Index = UV_Index_Module(appid=appid, lat=lat, lon=lon, cnt=cnt)

# Latitude and Longitude of Harper College
UV_Index.appid = app.config['OPENWEATHERMAP_API_KEY']
UV_Index.lat = 42.0811
UV_Index.lon = 88.0729
UV_Index.cnt = 1

print(UV_Index.get_json())

# This will print a link to the needed JSON data for the UV Index.