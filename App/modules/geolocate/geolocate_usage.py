from App.modules.geolocate.geolocate import GeoLocate

city = 'warsaw'
region = 'poland'

geo_locate = GeoLocate()

# country_code = geo_locate.get_country_code(region)
# country_name = geo_locate.get_country_name(region)
#
# result = geo_locate.get_lat_lon(city, country_code)
# print()
# if result:
#     print(f'Lat: {result["lat"]}')
#     print(f'Lon: {result["lon"]}')
# else:
#     print('Invalid location')

# print(geo_locate.rapid_api('ChiCaGo', None, 'uS'))
print(geo_locate.test_method())