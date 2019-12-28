from flask import render_template, request, jsonify, Blueprint
from App.modules.geolocate.geolocate import GeoLocate
from App.modules.helper.helper import prepare_data
from App import app

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/api/weather', methods=['GET'])
def get_weather():
    user_input = request.args.get('name')

    if ',' in user_input:
        user_input = user_input.split(',')
        if len(user_input) is 2:
            city = user_input[0].strip(' ').lower()
            region = user_input[1].strip(' ').lower()
        else:
            return jsonify({'error': 'Input Error',
                            'error_msg': 'Please enter a Zip Code or Location(City, State) or (City, Country)'})
    else:
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

    data = prepare_data(location_info)
    return jsonify({'api_response': data})


@app.route('/api/geolocate/coordinates', methods=['GET'])
def geolocate_coordinates():
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    geolocate = GeoLocate()
    results = geolocate.reverse_geocode(lat, lon)

    if results:
        return jsonify({'api_response': results})
    else:
        return jsonify({'error': 'Geolocation Error', 'error_msg': 'Could not find city based on your coordinates!'})


@app.route('/api/geolocate/zip', methods=['GET'])
def geolocate_zip():
    zip_code = request.args.get('zip')
    print(f'ZIP: {zip_code}')

    geolocate = GeoLocate()
    results = geolocate.zip_geocode(zip_code)

    if results:
        return jsonify({'api_response': results})
    else:
        return jsonify(
            {
                'error': 'Geolocation Error',
                'error_msg': f'Could not find city based on the provided zip code [{zip_code}]'
            })


@main.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
