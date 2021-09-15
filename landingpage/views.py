import json

from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from api.models import VaccineCenter


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
        center = json.loads(center.replace(" lat", '"lat"').replace(" lng", '"lng"'))
        location = [center['lat'], center['lng']]
        from api.utils import find_closest_facilities
        nearest_facilities = find_closest_facilities(location)
        self.context.update({'facilities': nearest_facilities})
        return render(request, self.template_name, context=self.context)
