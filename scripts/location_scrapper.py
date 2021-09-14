import requests
import pymysql.cursors

from api.models import SubCounty


def run():
    scrape_subcounties()


def scrape_subcounties():
    google_api_key = ''
    from api.models import County
    counties = County.objects.all()
    for county in counties:
        subcounties = SubCounty.objects.filter(county=county)
        places_search_path = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?radius=50000' \
                             '&key=' + google_api_key
        for subcounty in subcounties:
            response = requests.get(places_search_path + "&name=" + subcounty.name + "&location=" + county.location).json()
            results = response['results']
            if len(results) > 0:
                place = results[0]
                location = str(place['geometry']['location']['lat']) + ',' + str(place['geometry']['location']['lng'])
                subcounty.location = location
                subcounty.save()
            else:
                print("404 - ", str(subcounty.name), subcounty.id)
