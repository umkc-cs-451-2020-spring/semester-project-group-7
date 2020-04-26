from django.apps import AppConfig


class OnlinebankingConfig(AppConfig):
    name = 'onlinebanking'
    
    def ready(self):
        from . import signals
