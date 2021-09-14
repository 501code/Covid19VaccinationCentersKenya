import csv

from api.models import County, SubCounty, VaccineCenter


def run():
    latest_file = csv.reader(open("static/c19vaccinecenters_2021_08.csv", "r"))
    counties = []
    sub_counties = []
    facilities = []
    sub_counties_dict = []
    for row in latest_file:
        county = row[0].title()
        if county not in counties:
            counties.append(county)
        sub_county = row[1].lower().replace(" sub county", ""). \
            replace(" subcounty", "").title()
        if sub_county not in sub_counties:
            sub_counties.append(sub_county)
            sub_counties_dict.append({'County': county, 'Sub-county': sub_county})
        facilities.append({'County': county, 'Sub-county': sub_county, 'Facility': row[2].title()})

    add = []
    for missing in sub_counties:
        if not SubCounty.objects.filter(name=missing).exists():
            sub1 = SubCounty()
            sub1.name = missing
            try:
                for s in sub_counties_dict:
                    if s['Sub-county'] == missing:
                        county_name = s['County']
                        break
                sub1.county = County.objects.get(name__icontains=county_name)
                add.append(sub1)
            except Exception as e:
                print(s['Sub-county'], missing, e)
    SubCounty.objects.bulk_create(add)

    add = []
    for fac in facilities:
        try:
            vc = VaccineCenter()
            vc.name = fac['Facility']
            vc.sub_county = SubCounty.objects.filter(name=fac['Sub-county']).first()
            add.append(vc)
        except Exception as e:
            print(fac, e)
            raise e
    VaccineCenter.objects.bulk_create(add)
