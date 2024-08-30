from django.urls import re_path
from web import consumers

websocket_urlpatterns = [
    re_path(r'^publish/(?P<task_id>\d+)/$', consumers.PublishConsumer.as_asgi()),
]
