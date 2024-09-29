from django.apps import AppConfig

from .chroma import get_chroma_client


class BotFaceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bot_face'
    verbose_name = 'Bot Face'

    def ready(self):
        chroma_client = get_chroma_client()
        chroma_client.heartbeat()
