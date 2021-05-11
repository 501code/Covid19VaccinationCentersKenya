import requests
import pymysql.cursors


def run():
    google_api_key = 'MAPS_API_KEY'
    places_search_path = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?radius=50000' \
                        '&type=hospital&key=' + google_api_key

    # Connect to the database
    cnx = pymysql.connect(host="localhost",
                                 user="root",
                                 password="root",
                                 db="c19_vaccine_centers",
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    with cnx.cursor() as cur:
        cur.execute("SELECT * FROM centers")
        for places in cur.fetchall():
            place_id = places['id']
            area_name = places['name']
            county_center = places['county_center']
            response = requests.get(places_search_path + "&name=" + area_name + "&location=" + county_center).json()
            results = response['results']
            if len(results) > 0:
                place = results[0]
                location = str(place['geometry']['location']['lat']) + ',' + str(place['geometry']['location']['lng'])
                # update db
                query_string = "UPDATE centers SET county_center = %s WHERE id=" + str(place_id)
                cur.execute(query_string, (location,))
                cnx.commit()
                print("200 - " + str(place_id) + area_name)

            else:
                print("404 - " + str(place_id) + area_name)
            cnx.commit()

