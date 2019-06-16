import json
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.http import (
    HttpResponse,
    JsonResponse,
)
from django.utils.decorators import method_decorator
from django.views import generic as generic_views
from django.views.decorators.csrf import csrf_exempt

from gis_route_calculator.apps.routes.models import (
    Route,
)
from gis_route_calculator.utils.dates import datetime_range_for_day


@method_decorator(csrf_exempt, name='post')
class RouteView(generic_views.View):

    def post(self, request, *args, **kwargs):
        route = Route()
        route.save()
        return JsonResponse({
            'route_id': route.route_id
        })


class WayPointView(generic_views.View):

    def post(self, request, route_id: int, *args, **kwargs):
        way_point_json = json.loads(request.body)
        try:
            route = Route.get_route_within_date_range(
                route_id,
                datetime_range_for_day(datetime.utcnow())
            )
        except ObjectDoesNotExist:
            return HttpResponse(
                status=400,
                reason='Route does not exist or was created too long ago.'
            )
        route.add_way_point(way_point_json)
        return JsonResponse({})


class RouteLengthView(generic_views.View):

    def get(self, request, route_id: int, *args, **kwargs):
        route = Route.objects.get(route_id=route_id)
        return JsonResponse({
            'km': route.length
        })


class LongestRouteForEachDay(generic_views.View):

    def get(self, request):
        # I simply don't know how to do this with django
        # spent hour or something like that, trying to find out.
        routes_per_day = Route.objects.raw(
            '''
            SELECT date(created) AS day,
                   MAX(routes_route.length) AS length_max,
                   route_id
            FROM routes_route GROUP BY day
            '''
        )
        return JsonResponse(
            {
                route.day: {
                    'route_id': route.route_id,
                    'length': route.length
                }
                for route in routes_per_day
            }
        )
