import collections
import itertools


def find_closest_facilities(origin):
    from api.models import VaccineCenter
    facilities = VaccineCenter.objects.filter(location__isnull=False)
    facilities_distances = {}
    for facility in facilities:
        loc = facility.location.split(",")
        distance = (float(loc[0]) - origin[0])**2 + (float(loc[1]) - origin[1])**2
        facilities_distances.update({distance: facility})
    facilities_distances = collections.OrderedDict(sorted(facilities_distances.items()))
    closest_facilities = dict(itertools.islice(facilities_distances.items(), 10))
    return [facility for distance, facility in closest_facilities.items()]
