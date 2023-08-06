import uuid

import pytest
import requests
from app.models import Customer
from app.models import Invoice
from app.models import Product
from django.urls import reverse

# pylint: skip-file


"""
These tests exist to make sure the application we use to test, actually works.
These tests do not test `django-partitioned-audit` functionality.
"""


@pytest.mark.django_db(transaction=True)
def test_create_customer_works_with_audit_disabled(live_server, remove_auditing):
    name = str(uuid.uuid4())
    response = requests.post(f"{live_server}{reverse('customer/create')}", data=dict(name=name))
    response.raise_for_status()
    assert Customer.objects.filter(name=name).exists()


@pytest.mark.django_db(transaction=True)
def test_update_customer_works_with_audit_disabled(live_server, remove_auditing):
    orig_name = str(uuid.uuid4())
    new_name = str(uuid.uuid4())
    customer = Customer.objects.create(name=orig_name)
    assert Customer.objects.filter(name=orig_name).exists()

    request_url = f"{live_server}{reverse('customer/update', args=[customer.pk])}"
    response = requests.post(request_url, data=dict(name=new_name))
    response.raise_for_status()
    assert not Customer.objects.filter(name=orig_name).exists()
    assert Customer.objects.filter(name=new_name).exists()


@pytest.mark.django_db(transaction=True)
def test_create_invoice_works_with_audit_disabled(live_server, remove_auditing):
    name = str(uuid.uuid4())
    response = requests.post(f"{live_server}{reverse('invoice/create')}", data=dict(name=name))
    response.raise_for_status()
    assert Invoice.objects.filter(name=name).exists()


@pytest.mark.django_db(transaction=True)
def test_create_product_works_with_audit_disabled(live_server, remove_auditing):
    name = str(uuid.uuid4())
    response = requests.post(f"{live_server}{reverse('product/create')}", data=dict(name=name))
    response.raise_for_status()
    assert Product.objects.filter(name=name).exists()
