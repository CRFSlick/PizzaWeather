from App import app
import requests
# import zipcodes
import json
import os


class GeoLocate(object):

    def __init__(self):
        pass

    @staticmethod
    def get_file_handle(path_list):
        """
        Gets file handle for opening

        Args:
            path_list (list)

        Returns:
            file_path

        Raises:
            FileNotFoundError
        """
        try:
            current_path = os.path.dirname(__file__)
            if '\\' in current_path:
                slash = '\\'
            elif '/' in current_path:
                slash = '/'
            else:
                slash = '/'
            path = slash.join(path_list)
            if os.path.dirname(__file__).split(slash)[-1] != 'App':
                file_path = os.path.dirname(__file__)[0:os.path.dirname(__file__).find(f'{slash}App{slash}') +
                                                        len(f'{slash}App{slash}')] + path
            else:
                file_path = os.path.dirname(__file__) + path
            if os.path.exists(file_path):
                return file_path
            else:
                raise FileNotFoundError
        except FileNotFoundError:
            raise FileNotFoundError(f'could not open file {path}')

    def get_country_code(self, country):
        """
        Gets country code given country

        Args:
            country (str)

        Returns:
            country_code (str)
        """
        iso_3116 = json.loads(open(self.get_file_handle(['resources', 'json', 'ISO_3116.json']), 'r').read())

        if len(country) == 2:
            for country_info in iso_3116:
                if country_info['iso_3166-2'].split(':')[1] == country.upper():
                    return country_info['iso_3166-2'].split(':')[1]

        for country_info in iso_3116:
            if country_info['name'].lower() == country.lower():
                return country_info['iso_3166-2'].split(':')[1]

        raise ValueError(f'could not find ISO_3116 country code for country "{country}", please enter a valid country '
                         f'name or country code')

    def get_country_name(self, country):
        """
        Gets country name for a given country

        Args:
            country (str)

        Returns:
            country_name (str)
        """
        iso_3116 = json.loads(open(self.get_file_handle(['resources', 'json', 'ISO_3116.json']), 'r').read())

        for country_info in iso_3116:
            if country_info['iso_3166-2'].split(':')[1] == country.upper():
                return country_info['name']

        for country_info in iso_3116:
            if country_info['name'].lower() == country.lower():
                return country_info['name']

        raise ValueError(f'could not find ISO_3116 country name for country "{country}", please enter a valid country '
                         f'name or country code')

    def get_location_info(self, city, origional_region):
        """
        Gets information about a given city region combination if possible

        Args:
            city (str)
            origional_region(str)

        Returns:
            {'display_name': f'{city}, {display_region}', 'city': city, 'region': region,
            'country': country, 'lat': lat, 'lon': lon} (dict)

            OR

            None
        """
        region = origional_region.lower()

        states_dict = json.loads(
            open(self.get_file_handle(['resources', 'json', 'states.json']), 'r', encoding='UTF-8').read())
        countries_dict = json.loads(
            open(self.get_file_handle(['resources', 'json', 'ISO_3116.json']), 'r', encoding='UTF-8').read())

        for state in states_dict:
            if state['name'].lower() == region or state['abbreviation'].lower() == region:
                region = state['name']
                country = 'US'.lower()
                display_region = state['abbreviation']

                country_full = self.get_country_name(country)
                result = self.forward_geocode(city, display_region, country)

                if result:
                    lat = result['lat']
                    lon = result['lon']
                    city_name = result['city_name']
                    region = result['region_name']

                    return {'display_name': f'{city_name}, {display_region}', 'city': city_name, 'region': region,
                            'country': country_full, 'lat': lat, 'lon': lon}

        for country_info in countries_dict:
            if country_info['name'].lower() == region or country_info['alpha-2'].lower() == origional_region.lower():
                country = country_info['name']
                display_region = country_info['alpha-2']

                if display_region.upper() == 'US':

                    country_full = self.get_country_name(country)

                    for state in states_dict:
                        if state['name'].lower() == region.lower() or state['abbreviation'].lower() == \
                                region.lower():
                            display_region = state['abbreviation']

                    result = self.forward_geocode(city, None, display_region)

                    if result:
                        lat = result['lat']
                        lon = result['lon']
                        city_name = result['city_name']
                        region = result['region_name']

                        for state in states_dict:
                            if state['name'].lower() == region.lower() or state['abbreviation'].lower() == region.lower():
                                display_region = state['abbreviation']

                        return {'display_name': f'{city_name}, {display_region}', 'city': city_name,
                                'region': display_region, 'country': country_full, 'lat': lat, 'lon': lon}

                else:
                    result = self.forward_geocode(city, None, display_region)

                    if result:
                        lat = result['lat']
                        lon = result['lon']
                        city_name = result['city_name']

                        return {'display_name': f'{city_name}, {display_region}', 'city': city_name,
                                'region': display_region, 'country': country, 'lat': lat, 'lon': lon}

    def get_lat_lon(self, city, region_dict):
        """
        Gets latitude/longitude for a given city region combination

        Args:
            city (str)
            region_dict (dict)

        Returns:
            {'lat': lat], 'lon': lon}

            OR

            None
        """
        results = []
        region = region_dict['abbreviation']
        region_type = region_dict['type']

        if region_type == 'state':
            us_cities = zipcodes.filter_by()
            for entry in us_cities:
                if entry['city'].lower() == city.lower() and entry['state'].lower() == region.lower():
                    results.append(entry)
            if results != []:
                return {'lat': results[0]['lat'], 'lon': results[0]['long']}

        elif region_type == 'country':
            country_dict = json.loads(open(self.get_file_handle(['resources', 'json', 'cities.json']), 'r',
                                           encoding='UTF-8').read())
            for entry in country_dict:
                if entry['name'].lower() == city.lower() and entry['country'].lower() == region.lower():
                    results.append(entry)
            if results != []:
                if len(results) == 1:
                    return {'lat': results[0]['lat'], 'lon': results[0]['lng']}

    @staticmethod
    def forward_geocode(city, region, country):
        """
        Forward geocodes location to lat / lon for use in other API

        Args:
            city (str)
            region (str or None)
            country (str)

        Returns:
            location_info OR None
        """

        city = city.lower().strip()
        country = country.lower().strip()

        if region:
            region = region.lower()

        url = 'http://open.mapquestapi.com/geocoding/v1/address'

        params = {
            'key': app.config['RAPID_API_KEY'],
            'location': f'{city}, {country}'
        }

        r = requests.get(url=url, params=params)

        if r.status_code == 200:
            data = json.loads(r.text)

            count = 0
            result_count = len(data['results'][0]['locations']) - 1

            while count < result_count:
                city_name = data['results'][0]['locations'][count]['adminArea5'].strip()
                region_name = data['results'][0]['locations'][count]['adminArea3'].strip()
                country_name = data['results'][0]['locations'][count]['adminArea1'].strip()
                lat = data['results'][0]['locations'][count]['latLng']['lat']
                lon = data['results'][0]['locations'][count]['latLng']['lng']

                # DEBUG OUTPUT
                # print(data['results'][0]['locations'])
                # print(f'{city_name}: {city}')
                # print(f'{region_name}: {region}')
                # print(f'{country_name}: {country}')

                if city_name.lower() == city and region_name.lower() == region and country_name.lower() == country:
                    return {'city_name': city_name, 'region_name': region_name, 'country_name': country_name,
                            'lat': lat, 'lon': lon}
                elif not region:
                    if city_name.lower() == city and country_name.lower() == country:
                        return {'city_name': city_name, 'region_name': region_name, 'country_name': country_name,
                                'lat': lat, 'lon': lon}

                count += 1

    @staticmethod
    def reverse_geocode(lat, lon):
        """
        Reverse geocodes location to lat / lon for use in other API

        Args:
            lat (float)
            lon (float)
        Returns:
            location_info OR None
        """

        url = 'http://open.mapquestapi.com/geocoding/v1/address'

        params = {
            'key': app.config['RAPID_API_KEY'],
            'location': f'{lat}, {lon}'
        }

        r = requests.get(url=url, params=params)

        if r.status_code == 200:
            data = json.loads(r.text)

            if data['results'][0]['locations'][0]:
                city_name = data['results'][0]['locations'][0]['adminArea5'].strip()
                region_name = data['results'][0]['locations'][0]['adminArea3'].strip()
                country_name = data['results'][0]['locations'][0]['adminArea1'].strip()
                lat = data['results'][0]['locations'][0]['latLng']['lat']
                lon = data['results'][0]['locations'][0]['latLng']['lng']

                # DEBUG OUTPUT
                # print(data['results'][0]['locations'])
                # print(f'{city_name}')
                # print(f'{region_name}')
                # print(f'{country_name}')

                if country_name == 'US':
                    return {'city_name': city_name, 'region_name': region_name, 'country_name': country_name,
                            'display_name': f'{city_name}, {region_name}', 'lat': lat, 'lon': lon}
                else:
                    return {'city_name': city_name, 'region_name': region_name, 'country_name': country_name,
                            'display_name': f'{city_name}, {country_name}', 'lat': lat, 'lon': lon}

    @staticmethod
    def zip_geocode(zip_code):
        """
        Forward geocodes location to lat / lon for use in other API

        Args:
            zip_code (int)

        Returns:
            location_info OR None
        """

        url = 'http://open.mapquestapi.com/geocoding/v1/address'

        params = {
            'key': app.config['RAPID_API_KEY'],
            'location': f'{zip_code}'
        }

        r = requests.get(url=url, params=params)

        if r.status_code == 200:
            data = json.loads(r.text)

            count = 0
            result_count = len(data['results'][0]['locations']) - 1

            while count < result_count:
                city_name = data['results'][0]['locations'][count]['adminArea5'].strip()
                region_name = data['results'][0]['locations'][count]['adminArea3'].strip()
                country_name = data['results'][0]['locations'][count]['adminArea1'].strip()
                lat = data['results'][0]['locations'][count]['latLng']['lat']
                lon = data['results'][0]['locations'][count]['latLng']['lng']

                # DEBUG OUTPUT
                # print(data['results'][0]['locations'])
                print(f'{city_name}')
                print(f'{region_name}')
                print(f'{country_name}')

                if city_name != '' and region_name != '' and country_name != '':

                    if country_name == 'US':
                        return {'city_name': city_name, 'region_name': region_name, 'country_name': country_name,
                                'display_name': f'{city_name}, {region_name}', 'lat': lat, 'lon': lon}
                    else:
                        return {'city_name': city_name, 'region_name': region_name, 'country_name': country_name,
                                'display_name': f'{city_name}, {country_name}', 'lat': lat, 'lon': lon}

                count += 1
