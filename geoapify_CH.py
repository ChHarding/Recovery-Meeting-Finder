import requests
from requests.structures import CaseInsensitiveDict

def geoapify(searchText, apiKey):
    url = "https://api.geoapify.com/v1/geocode/search?text=" + searchText + "&limit=100&&filter=countrycode:us&apiKey=" + apiKey

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"

    resp = requests.get(url, headers=headers)

    json = resp.json()


    places = json['features']
    numberOfPlaces = len(places)

    #print(numberOfPlaces)

    name = city = county = state = country = country_code = ""
    formatted = lat = lon = result_type = confidence = ""
    confidence_city_level = match_type = ""


    if numberOfPlaces > 0:

        if 'name' in places[0]['properties'].keys():
            name = places[0]['properties']['name']

        if 'city' in places[0]['properties'].keys():
            city = places[0]['properties']['city']

        if 'county' in places[0]['properties'].keys():
            county = places[0]['properties']['county']

        if 'state' in places[0]['properties'].keys():
            state = places[0]['properties']['state']

        if 'country' in places[0]['properties'].keys():
            country = places[0]['properties']['country']

        if 'country_code' in places[0]['properties'].keys():
            country_code = places[0]['properties']['country_code']

        if 'formatted' in places[0]['properties'].keys():
            formatted = places[0]['properties']['formatted']

        if 'lon' in places[0]['properties'].keys():
            lon = places[0]['properties']['lon']

        if 'lat' in places[0]['properties'].keys():
            lat = places[0]['properties']['lat']

        if 'result_type' in places[0]['properties'].keys():
            result_type = places[0]['properties']['result_type']

        if 'confidence' in places[0]['properties']['rank'].keys():
            confidence = places[0]['properties']['rank']['confidence']

        if 'confidence_city_level' in places[0]['properties']['rank'].keys():
            confidence_city_level = places[0]['properties']['rank']['confidence_city_level']

        if 'match_type' in places[0]['properties']['rank'].keys():
            match_type = places[0]['properties']['rank']['match_type']

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
