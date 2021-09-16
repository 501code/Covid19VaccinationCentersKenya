import json

import requests
from django.conf import settings
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt


class LandingPage(View):
    def __init__(self):
        self.template_name = 'landingpage/locate.html'
        self.context = {
            'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY,
        }
        super().__init__()

    def get(self, request):
        return render(request, self.template_name, context=self.context)

    @csrf_exempt
    def post(self, request):
        center = request.POST.get('center')
        location = None
        if center:
            center = json.loads(center.replace(" lat", '"lat"').replace(" lng", '"lng"'))
            location = [center['lat'], center['lng']]
        else:
            # try free text search
            facility_address = request.POST.get('facility-address')
            url = "https://maps.googleapis.com/maps/api/place/textsearch/json?key=" + settings.GOOGLE_MAPS_API_KEY \
                  + "&query=" + facility_address
            response = requests.get(url).json()
            results = response['results']
            if len(results) > 0:
                place = results[0]
                location = [float(place['geometry']['location']['lat']), float(place['geometry']['location']['lng'])]
            else:
                self.context.update({'error_message': 'Location not found!'})
        if location:
            from api.utils import find_closest_facilities
            nearest_facilities = find_closest_facilities(location)
            self.context.update({'facilities': nearest_facilities})
        return render(request, self.template_name, context=self.context)
