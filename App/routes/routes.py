from flask import render_template, request, jsonify, Blueprint
from App.modules.geolocate.geolocate import GeoLocate
from App.modules.helper.helper import unix_to_12_hr_time
from App.modules.helper.helper import get_local_time
from App.modules.helper.helper import get_local_date
from App.modules.api.api import API
from App import app
# import reverse_geocoder as rg
import sys
import os

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/api/weather', methods=['GET'])
def get_weather():
    user_input = request.args.get('name')

    if ',' in user_input:
        user_input = user_input.split(',')

        if len(user_input) is not 2:
            return jsonify({'error': 'Input Error',
                            'error_msg': 'Please enter a Zip Code or Location(City, State) or (City, Country)'})

        city = user_input[0].strip(' ').lower()
        region = user_input[1].strip(' ').lower()
    else:
        try:
            zip_code = int(user_input)
            return jsonify({'error': 'Programmer Error',
                            'error_msg': f'Your input {zip_code} was a zip code! Too bad that it doesn\'t work yet :/'})
        except ValueError:
            return jsonify({'error': 'Input Error',
                            'error_msg': 'Please enter a Zip Code or Location(City, State) or (City, Country)'})

    geo_locate = GeoLocate()
    location_info = geo_locate.get_location_info(city, region)

    if not location_info:
        if len(region) == 2:
            region = region.upper()
        else:
            region = region.capitalize()
        city = city.capitalize()
        return jsonify({'error': 'Data Not Found Error',
                        'error_msg': f'Could not find weather data for [{city}, {region}]'})

    api = API(api_key=app.config['OPENWEATHERMAP_API_KEY'], lat=location_info["lat"], lon=location_info["lon"], days=7)
    radar_urls = api.get_radar_urls()

    lat = float(location_info["lat"])
    lon = float(location_info["lon"])
    city = location_info['city']
    region = location_info['region']
    country = location_info['country']
    display_name = location_info['display_name']
    dt_updated = unix_to_12_hr_time(api.current_weather[0]['datetime'], api.current_timezone_offset[0]['timezone_offset'])
    dt_sunrise = unix_to_12_hr_time(api.current_sunrise[0]['sunrise'], api.current_timezone_offset[0]['timezone_offset'])
    dt_sunset = unix_to_12_hr_time(api.current_sunset[0]['sunset'], api.current_timezone_offset[0]['timezone_offset'])
    dt_date = get_local_date(api.current_timezone_offset[0]['timezone_offset'])
    dt_time = get_local_time(api.current_timezone_offset[0]['timezone_offset'])
    weather = api.current_weather[0]['weather']
    weather_description = api.current_weather_description[0]['weather-description']
    weather_icon_url = api.current_weather_icon_url[0]['weather-icon-url']
    temperature = api.current_temperature_average[0]['kelvin']
    temperature_rounded = api.current_temperature_average[0]['kelvin']
    temperature_average = api.current_temperature_average[0]['kelvin']
    temperature_high = api.current_temperature_max[0]['kelvin']
    temperature_low = api.current_temperature_min[0]['kelvin']
    wind_speed = api.current_wind_speed[0]['wind-speed']
    wind_direction = api.current_wind_direction[0]['wind-direction']
    cloud_cover = api.current_cloud_cover[0]['cloud-cover']
    precipitation = api.current_precipitation[0]['precipitation']
    humidity = api.current_humidity[0]['humidity']
    # uv_index = api.uv_index_today[0]['uv-index']
    radar_base = radar_urls['base']
    radar_precipitation = radar_urls['precipitation']
    radar_temperature = radar_urls['temperature']
    radar_pressure = radar_urls['pressure']
    radar_clouds = radar_urls['clouds']
    radar_wind = radar_urls['wind']

    data = {
        'lat': lat,
        'lon': lon,
        'city': city,
        'region': region,
        'country': country,
        'dt_date': dt_date,
        'dt_time': dt_time,
        'dt_updated': dt_updated,
        'dt_sunrise': dt_sunrise,
        'dt_sunset': dt_sunset,
        'weather': weather,
        'display_name': display_name,
        'weather_description': weather_description,
        'weather_icon_url': weather_icon_url,
        'temperature': temperature,
        'temperature_rounded': temperature_rounded,
        'temperature_average': temperature_average,
        'temperature_high': temperature_high,
        'temperature_low': temperature_low,
        'wind_speed': wind_speed,
        'wind_direction': wind_direction,
        'cloud_cover': cloud_cover,
        'precipitation': precipitation,
        'humidity': humidity,
        'uv_index': None,
        'radar_base': radar_base,
        'radar_precipitation': radar_precipitation,
        'radar_temperature': radar_temperature,
        'radar_pressure': radar_pressure,
        'radar_clouds': radar_clouds,
        'radar_wind': radar_wind
    }

    print(data)

    if user_input:
        return jsonify({'api_response': data})

    return jsonify({'error': 'Input Error',
                    'error_msg': 'Missing data!'})


@app.route('/api/locate', methods=['GET'])
def locate():
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    geolocate = GeoLocate()
    results = geolocate.reverse_geocode(lat, lon)

    if results:
        return jsonify({'api_response': results})
    else:
        return jsonify({'error': 'Geolocation Error', 'error_msg': 'Could not find city based on your coordinates!'})


@main.errorhandler(404)
def page_not_found(e):
    return render_template('404-2.html'), 404


def block_print():
    sys.stdout = open(os.devnull, 'w')


def enable_print():
    sys.stdout = sys.__stdout__


def convert_odict_to_dict(odict):
    dict = {}
    for key, value in odict.items():
        dict[key] = value

    if dict['cc'].lower() == 'us':
        dict['display_name'] = f'{dict["name"]}, {dict["admin1"]}'
    else:
        dict['display_name'] = f'{dict["name"]}, {dict["cc"]}'

    return dict
