from django.urls import (
    include,
    path,
)

from gis_route_calculator.apps.routes.urls import urlpatterns as routes_urlpatterns

urlpatterns = [
    path('route/', include(routes_urlpatterns))
]
