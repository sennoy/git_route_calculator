import typing

from geopy.distance import geodesic


def distance_between_two_points(point1: typing.Tuple[float, float],
                                point2: typing.Tuple[float, float]) -> geodesic:
    return geodesic(
        point1,
        point2
    )


def km_between_two_points(point1: typing.Tuple[float, float],
                          point2: typing.Tuple[float, float]) -> float:
    return distance_between_two_points(point1, point2).km


def km_between_two_way_points(way_point1, way_point2):
    return km_between_two_points(
        way_point1.lat_lon_tuple(),
        way_point2.lat_lon_tuple(),
    )
