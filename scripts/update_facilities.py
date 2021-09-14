import csv

from api.models import County


def run():
    latest_file = csv.reader(open("static/c19vaccinecenters_2021_08.csv", "r"))
    counties = []
    sub_counties = []
    facilities = []
    for row in latest_file:
        county = row[0].title()
        counties.append(county)
        sub_county = row[1].title()
        sub_counties.append(sub_county)
        facilities.append({'County': county, 'Sub-county': sub_county, 'Facility': row[2].title()})

    # check counties that don't exist
    missing_counties_list = County.objects.exclude(name__in=counties)
    print(missing_counties_list)