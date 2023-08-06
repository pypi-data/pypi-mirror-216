import uuid

from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=False)


class Product(models.Model):
    product_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)


class Invoice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)


class InvoiceItem(models.Model):
    name = models.CharField(max_length=100)
