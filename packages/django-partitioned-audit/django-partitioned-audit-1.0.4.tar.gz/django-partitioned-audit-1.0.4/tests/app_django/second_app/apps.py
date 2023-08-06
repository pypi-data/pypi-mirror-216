from django.apps import AppConfig


class SecondaryAppConfig(AppConfig):
    name = "second_app"
    trigger_audit_models = [
        "Customer",
        "Product",
        "Invoice",
    ]
