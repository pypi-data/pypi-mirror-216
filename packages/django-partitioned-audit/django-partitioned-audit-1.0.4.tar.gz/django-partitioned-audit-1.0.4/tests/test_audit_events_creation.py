import uuid

import pytest
import requests
from app.models import Customer
from django.urls import reverse

from django_partitioned_audit.audit_table.advanced_audit_table_manager import AdvancedAuditTableManager
from django_partitioned_audit.audit_table.simple_audit_table_manager import SimpleAuditTableManager
from django_partitioned_audit.models import AdvancedAuditEntry
from django_partitioned_audit.models import Operation
from django_partitioned_audit.models import SimpleAuditEntry

# pylint: skip-file


@pytest.mark.parametrize(
    "audit_table_manager_class,model_class",
    [[SimpleAuditTableManager, SimpleAuditEntry], [AdvancedAuditTableManager, AdvancedAuditEntry]],
)
def test_create(audit_table_manager_class, model_class, live_server, use_audit_table_manager):
    use_audit_table_manager(audit_table_manager_class, [Customer])
    assert model_class.objects.all().count() == 0

    name = str(uuid.uuid4())
    data = dict(name=name)
    response = requests.post(f"{live_server}{reverse('customer/create')}", data=data)
    response.raise_for_status()
    assert Customer.objects.filter(name=name).exists()

    # Assert model was created and audit exists
    audit_entry = model_class.objects.all().get()
    assert audit_entry.is_insert()
    assert audit_entry.get_row_data()["name"] == name


@pytest.mark.parametrize(
    "audit_table_manager_class,model_class",
    [[SimpleAuditTableManager, SimpleAuditEntry], [AdvancedAuditTableManager, AdvancedAuditEntry]],
)
def test_update(audit_table_manager_class, model_class, live_server, use_audit_table_manager):
    use_audit_table_manager(audit_table_manager_class, [Customer])

    original_name = str(uuid.uuid4())
    customer = Customer.objects.create(name=original_name)

    new_name = str(uuid.uuid4())
    data = dict(name=new_name)
    response = requests.post(f"{live_server}{reverse('customer/update', args=[customer.pk])}", data=data)
    response.raise_for_status()
    assert Customer.objects.filter(name=new_name).exists()

    # Assert model was created and audit exists
    audit_entry = model_class.objects.filter_operation(Operation.UPDATE).get()
    assert audit_entry.is_update()
    assert audit_entry.get_row_data()["name"] == new_name


@pytest.mark.parametrize(
    "audit_table_manager_class,model_class",
    [[SimpleAuditTableManager, SimpleAuditEntry], [AdvancedAuditTableManager, AdvancedAuditEntry]],
)
def test_delete(audit_table_manager_class, model_class, live_server, use_audit_table_manager):
    use_audit_table_manager(audit_table_manager_class, [Customer])

    name = str(uuid.uuid4())
    customer = Customer.objects.create(name=name)

    response = requests.post(f"{live_server}{reverse('customer/delete', args=[customer.pk])}")
    response.raise_for_status()
    assert not Customer.objects.filter(name=name).exists()

    # Assert model was created and audit exists
    audit_entry = model_class.objects.filter_operation(Operation.DELETE).get()
    assert audit_entry.is_delete()
    assert audit_entry.get_row_data()["name"] == name
