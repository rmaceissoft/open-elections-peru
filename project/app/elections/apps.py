from django.apps import AppConfig


class Config(AppConfig):
    name = "app.elections"
    label = "app_elections"
    verbose_name = "Elections"

    def ready(self):
        pass
