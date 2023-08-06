import uuid

import pytest
import requests
from app.models import Invoice
from app.models import Product
from django.urls import reverse

from django_partitioned_audit.models import SimpleAuditEntry
from tests.conftest import skipifadvanced

# pylint: skip-file


@skipifadvanced
@pytest.mark.django_db(transaction=True)
def test_pk_named_product_id(live_server, partition_created):
    name = str(uuid.uuid4())
    response = requests.post(f"{live_server}{reverse('product/create')}", data=dict(name=name))
    response.raise_for_status()
    assert Product.objects.filter(name=name).exists()

    # Assert model was created and audit exists
    audit_entry: SimpleAuditEntry = SimpleAuditEntry.objects.all().get()
    assert audit_entry.is_insert()
    assert audit_entry.get_row_data()["product_id"]
    assert audit_entry.get_row_data()["name"] == name


@skipifadvanced
@pytest.mark.django_db(transaction=True)
def test_pk_is_uuid(live_server, partition_created):
    name = str(uuid.uuid4())
    response = requests.post(f"{live_server}{reverse('invoice/create')}", data=dict(name=name))
    response.raise_for_status()
    assert Invoice.objects.filter(name=name).exists()

    # Assert model was created and audit exists
    audit_entry: SimpleAuditEntry = SimpleAuditEntry.objects.all().get()
    assert audit_entry.is_insert()
    assert audit_entry.get_row_data()["id"]
    assert audit_entry.get_row_data()["name"] == name
