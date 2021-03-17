from django.apps import AppConfig


class Config(AppConfig):
    name = "app.api"
    label = "app_api"
    verbose_name = "Api"

    def ready(self):
        pass
