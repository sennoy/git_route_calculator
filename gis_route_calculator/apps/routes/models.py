import typing

from django.db import models

from gis_route_calculator.gis_math.distance.geodesic import km_between_two_way_points
from gis_route_calculator.utils.dates import DateTimeRange


class Route(models.Model):
    route_id = models.AutoField(primary_key=True)
    length = models.IntegerField(default=0)

    created = models.DateTimeField(auto_now=True)

    @staticmethod
    def get_route_within_date_range(route_id: int,
                                    date_range: DateTimeRange):
        return Route.objects.get(
            route_id=route_id,
            created__gte=date_range.left,
            created__lt=date_range.right,
        )

    def add_way_point(self, way_point: typing.Dict[str, float]):
        way_point = WayPoint(route=self, **way_point)
        try:
            prev_way_point = self.waypoint_set.latest()
        except WayPoint.DoesNotExist:
            # first way point added.
            pass
        else:
            distance = km_between_two_way_points(prev_way_point, way_point)
            self.length += distance
            self.save()
        way_point.save()


class WayPoint(models.Model):
    way_point_id = models.IntegerField(primary_key=True)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)

    lat = models.FloatField()
    lon = models.FloatField()

    created = models.DateTimeField(auto_now=True)

    class Meta:
        get_latest_by = 'created'

    def lat_lon_tuple(self):
        return self.lat, self.lon
