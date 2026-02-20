"""
ASGI config for reconnect project.
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reconnect.settings')

django_asgi_app = get_asgi_application()

from reconnect.routing import websocket_urlpatterns  # noqa: E402 — must import after django setup

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
