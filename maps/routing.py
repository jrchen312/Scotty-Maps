# maps/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/get_location/(?P<floor_id>\w+)/(?P<tag_id>\w+)/$", consumers.LocationConsumer.as_asgi()),
]