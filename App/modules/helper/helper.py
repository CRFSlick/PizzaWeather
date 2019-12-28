from App.modules.api.api import API
from datetime import datetime
from App import app
import requests
import base64


def prepare_data(location_info):
    """
    Prepares data for API response

    Args:
        location_info (dict)

    Returns:
        data (dict)
    """

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
    radar_base = image_to_base64(radar_urls['base'])
    radar_precipitation = image_to_base64(radar_urls['precipitation'])
    radar_temperature = image_to_base64(radar_urls['temperature'])
    radar_pressure = image_to_base64(radar_urls['pressure'])
    radar_clouds = image_to_base64(radar_urls['clouds'])
    radar_wind = image_to_base64(radar_urls['wind'])

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

    return data


def unix_to_12_hr_time(unix_timestamp, offset):
    """
    Converts unix timestamp to 12 hour time

    Args:
        unix_timestamp (int)
        offset (int)
    """
    return datetime.utcfromtimestamp(unix_timestamp + offset).strftime('%I:%M %p').lstrip("0").replace(" 0", " ")


def unix_to_date(unix_timestamp, offset):
    """
    Converts unix timestamp to date

    Args:
        unix_timestamp (int)
        offset (int)
    """
    return datetime.utcfromtimestamp(unix_timestamp + offset).strftime('%m/%d/%Y')


def get_local_time(offset):
    """
    Gets local time given an offset from UTC time

    Args:
        offset (int)
    """
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    return datetime.utcfromtimestamp(timestamp + offset).strftime('%I:%M %p').lstrip("0").replace(" 0", " ")


def get_local_date(offset):
    """
    Gets local date given an offset from UTC time

    Args:
        offset (int)
    """
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    return datetime.utcfromtimestamp(timestamp + offset).strftime('%m/%d/%Y')


def image_to_base64(image_url):
    """
    Converts radar image URL to base64

    Args:
        image_url (str)
    """
    r = requests.get(image_url)
    if r.status_code == 200:
        image_data = base64.b64encode(r.content).decode('UTF-8')
        return image_data
