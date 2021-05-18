from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views import View

from api.models import VaccineCenter


class LandingPage(View):
    template_name = 'landingpage/result.html'

    def post(self, request):
        context = {}
        return render(request, self.template_name, context=context)

    def get(self, request):
        places = VaccineCenter.objects.exclude(Q(location__isnull=True) | Q(location=''))
        locs = []
        for place in places:
            loc = place.location
            loc1 = loc.split(",")[0].strip()
            loc2 = loc.split(",")[1].strip()
            locs.append({'name': place.name, 'loc1': loc1, 'loc2': loc2})
        center = request.POST.get('center', '{lat: '+locs[0]["loc1"]+', lng: '+locs[0]["loc2"]+'}')
        context = {
            'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY,
            'places': locs,
            'center': center
        }
        return render(request, self.template_name, context=context)
