from django.urls import (
    path,
    re_path,
)

from gis_route_calculator.apps.routes import views

urlpatterns = [
    path('', views.RouteView.as_view()),
    path('longest/per_day/', views.LongestRouteForEachDay.as_view()),
    re_path('^(?P<route_id>[0-9])/way_point/$', views.WayPointView.as_view()),
    re_path('^(?P<route_id>[0-9])/length/$', views.RouteLengthView.as_view()),

]
