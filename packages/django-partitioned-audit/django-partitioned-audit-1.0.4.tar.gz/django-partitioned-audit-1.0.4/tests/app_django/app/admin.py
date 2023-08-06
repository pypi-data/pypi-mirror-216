from app.models import Customer
from app.models import Invoice
from app.models import Product
from django.contrib import admin

from django_partitioned_audit.admin import TriggerAuditEntryAdmin
from django_partitioned_audit.models import SimpleAuditEntry


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(SimpleAuditEntry)
class CustomTriggerAuditEntryAdmin(TriggerAuditEntryAdmin):
    pass
