from django.apps import AppConfig


class Config(AppConfig):
    name = "app.shared"
    label = "app_shared"
    verbose_name = "Shared"

    def ready(self):
        pass
