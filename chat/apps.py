# chat/apps.py
from django.apps import AppConfig


class ChatsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat'

    def ready(self):
        import chat.signals  # Ensure signals are registered
