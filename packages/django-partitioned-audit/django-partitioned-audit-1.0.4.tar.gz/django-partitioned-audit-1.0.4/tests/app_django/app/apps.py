from django.apps import AppConfig


class AppConfig(AppConfig):
    name = "app"
    trigger_audit_models = [
        "Customer",
        "Product",
        "Invoice",
    ]
    audit_disabled = [
        "InvoiceItem",
    ]
