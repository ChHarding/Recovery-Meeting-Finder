'''
===========================================================
This class geocodes the addresses. Two parameters are passed
to this class: an address and an API key. Then, it uses a
third party service, namely Geoapify(https://www.geoapify.com/)
to get the coordinates of the address.
Geoapify is a paid service!

Input: searchText (or address), and apiKey
Output: Specifications of the searched address, including:
        name, city, county, state, country, country_code,
        formatted, lon, lat, result_type, confidence,
        confidence_city_level, match_type

Dependents: scraper_y12sr.py
Dependency: Geoapify service
==========================================================
'''

import requests
from requests.structures import CaseInsensitiveDict

def geoapify (searchText, apiKey):
    url = "https://api.geoapify.com/v1/geocode/search?text=" + searchText + "&limit=100&&filter=countrycode:us&apiKey=" + apiKey

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"

    resp = requests.get(url, headers=headers)

    json = resp.json()


    places = json['features']
    numberOfPlaces = len(places)


    # It might return more than one address.
    # So, we consider only the first one, which is the most likely correct address.

    if (numberOfPlaces>0):

        if ('name' in places[0]['properties'].keys()):
            name = places[0]['properties']['name']
        else:
            name = ""


        if ('city' in places[0]['properties'].keys()):
            city = places[0]['properties']['city']
        else:
            city = ""


        if ('county' in places[0]['properties'].keys()):
            county = places[0]['properties']['county']
        else:
            county = ""


        if ('state' in places[0]['properties'].keys()):
            state = places[0]['properties']['state']
        else:
            state = ""


        if ('country' in places[0]['properties'].keys()):
            country = places[0]['properties']['country']
        else:
            country = ""


        if ('country_code' in places[0]['properties'].keys()):
            country_code = places[0]['properties']['country_code']
        else:
            country_code = ""


        if ('formatted' in places[0]['properties'].keys()):
            formatted = places[0]['properties']['formatted']
        else:
            formatted = ""


        if ('lon' in places[0]['properties'].keys()):
            lon = places[0]['properties']['lon']
        else:
            lon = ""


        if ('lat' in places[0]['properties'].keys()):
            lat = places[0]['properties']['lat']
        else:
            lat = ""


        if ('result_type' in places[0]['properties'].keys()):
            result_type = places[0]['properties']['result_type']
        else:
            result_type = ""


        if ('confidence' in places[0]['properties']['rank'].keys()):
            confidence = places[0]['properties']['rank']['confidence']
        else:
            confidence = ""

        if ('confidence_city_level' in places[0]['properties']['rank'].keys()):
            confidence_city_level = places[0]['properties']['rank']['confidence_city_level']
        else:
            confidence_city_level = ""


        if ('match_type' in places[0]['properties']['rank'].keys()):
            match_type = places[0]['properties']['rank']['match_type']
        else:
            match_type = ""

        '''
        print(name)
        print(city)
        print(county)
        print(state)
        print(country)
        print(country_code)
        print(formatted)
        print(lon)
        print(lat)
        print(result_type)
        print(confidence)
        print(confidence_city_level)
        print(match_type)

        print(places[0]['properties'])
        '''

        return name, city, county, state, country, country_code, formatted, lon, lat, result_type, confidence, confidence_city_level, match_type


    else:
        return "", "", "", "", "", "", "", "", "", "", "", "", ""
