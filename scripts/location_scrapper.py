import requests
from api.models import SubCounty, VaccineCenter


def run():
    scrape_subcounties()
    scrape_hospitals()


def scrape_hospitals():
    google_api_key = ''
    from api.models import SubCounty
    subcounties = SubCounty.objects.all()
    for sub_county in subcounties:
        facilities = VaccineCenter.objects.filter(sub_county=sub_county, location__isnull=True)
        places_search_path = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?radius=50000' \
                             '&type=hospital&key=' + google_api_key
        for facility in facilities:
            url = places_search_path + "&name=" + facility.name + "&location=" + sub_county.location
            response = requests.get(url).json()
            results = response['results']
            if len(results) < 1:
                # try text search
                url = "https://maps.googleapis.com/maps/api/place/textsearch/json?key=" + google_api_key \
                      + "&query=" + facility.name
                response = requests.get(url).json()
                results = response['results']
            if len(results) > 0:
                place = results[0]
                location = str(place['geometry']['location']['lat']) + ',' + str(place['geometry']['location']['lng'])
                facility.location = location
                facility.save()
            else:
                print("404 - ", sub_county.name, str(facility.name), facility.id, url)


def scrape_subcounties():
    google_api_key = ''
    from api.models import County
    counties = County.objects.all()
    for county in counties:
        subcounties = SubCounty.objects.filter(county=county, location='')
        places_search_path = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?radius=50000' \
                             '&key=' + google_api_key
        for subcounty in subcounties:
            url = places_search_path + "&name=" + subcounty.name + "&location=" + county.location
            response = requests.get(url).json()
            results = response['results']
            if len(results) < 1:
                # try text search
                url = "https://maps.googleapis.com/maps/api/place/textsearch/json?key=" + google_api_key \
                      + "&query=" + subcounty.name
                response = requests.get(url).json()
                results = response['results']
            if len(results) > 0:
                place = results[0]
                location = str(place['geometry']['location']['lat']) + ',' + str(place['geometry']['location']['lng'])
                subcounty.location = location
                subcounty.save()
            else:
                print("404 - ", county.name, str(subcounty.name), subcounty.id, url)
