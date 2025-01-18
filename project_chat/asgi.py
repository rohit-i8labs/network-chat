"""
ASGI config for project_chat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/stable/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_chat.settings')

application = get_asgi_application()


# import os
# import django
# django.setup()   # very imp else will give error in ASGI
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# from channels.security.websocket import AllowedHostsOriginValidator
# from chat.routing import websocket_urlpatterns

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_chat.settings')

# # application = ProtocolTypeRouter({
# #     "http": get_asgi_application(),
# #     "websocket": AuthMiddlewareStack(
# #         URLRouter(websocket_urlpatterns)
# #     ),
# # })

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AllowedHostsOriginValidator(
#         URLRouter(websocket_urlpatterns)
#     ),
# })
