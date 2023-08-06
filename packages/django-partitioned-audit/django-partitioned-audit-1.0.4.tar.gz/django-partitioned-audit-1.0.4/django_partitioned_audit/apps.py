from django.apps import AppConfig


class SimpleTriggerAuditAppConfig(AppConfig):
    name = "django_partitioned_audit"

    def ready(self):
        pass
