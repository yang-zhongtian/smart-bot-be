from django.urls import re_path

from .consumers import HostConsumer, ClientCamConsumer, ClientCommandConsumer, ClientAnalyzeConsumer

websocket_urlpatterns = [
    re_path(r"ws/host/(?P<host_id>[-\w]+)/$", HostConsumer.as_asgi()),
    re_path(r"ws/client/(?P<host_id>[-\w]+)/cam/$", ClientCamConsumer.as_asgi()),
    re_path(r"ws/client/(?P<host_id>[-\w]+)/command/$", ClientCommandConsumer.as_asgi()),
    re_path(r"ws/client/(?P<host_id>[-\w]+)/analyze/$", ClientAnalyzeConsumer.as_asgi()),
]
