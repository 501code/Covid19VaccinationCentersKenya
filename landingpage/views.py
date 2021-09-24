import json

import requests
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from api.models import VaccineCenter, VaccineCenterFeedback


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


class Feedback(View):
    def __init__(self):
        self.template_name = 'landingpage/feedback.html'
        self.context = {
        }
        super().__init__()

    def get(self, request, **kwargs):
        facility = VaccineCenter.objects.get(id=kwargs['pk'])
        self.context.update({'facility': facility})
        return render(request, self.template_name, context=self.context)

    def post(self, request, *args, **kwargs):
        values = request.POST
        facility_id = values.get('facility')
        facility = VaccineCenter.objects.get(id=facility_id)
        additionalInfo = values.get("additionalInfo", None)
        waitingTime = values.get("waitingTime", 1)
        vaccineAvailable = values.get("vaccineAvailable", 'yes')

        # available vaccines
        jnj = values.get("jnj", None)
        moderna = values.get("moderna", None)
        pfizer = values.get("pfizer", None)
        astrazeneca = values.get("astrazeneca", None)
        vaccines = [jnj, moderna, pfizer, astrazeneca]
        vaccines = list(filter(lambda a: a!=None, vaccines)) # remove None

        # save feedback
        feedback = VaccineCenterFeedback()
        feedback.vaccine_center = facility
        feedback.additional_info = additionalInfo
        feedback.waiting_time = waitingTime
        feedback.vaccine_available = True if vaccineAvailable == "yes" else False
        feedback.vaccines = ",".join(vaccines)
        feedback.save()

        return HttpResponseRedirect("/")
