# mysite/asgi.py
import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from yangsuite.settings.base import prefs
from .urls import websocket_urlpatterns


os.environ.setdefault("DJANGO_SETTINGS_MODULE", prefs.get('settings_module'))

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
    }
)
