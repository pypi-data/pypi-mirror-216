import uuid

import pytest
import requests
from app.models import Customer
from django.db import OperationalError
from django.urls import reverse

from django_partitioned_audit.audit_table.advanced_audit_table_manager import AdvancedAuditTableManager
from django_partitioned_audit.audit_table.simple_audit_table_manager import SimpleAuditTableManager
from django_partitioned_audit.models import AdvancedAuditEntry
from django_partitioned_audit.models import SimpleAuditEntry

# pylint: skip-file


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize(
    "audit_table_manager_class,model_class",
    [[SimpleAuditTableManager, SimpleAuditEntry], [AdvancedAuditTableManager, AdvancedAuditEntry]],
)
def test_delete_audit_entries_fail(audit_table_manager_class, model_class, live_server, use_audit_table_manager):
    use_audit_table_manager(audit_table_manager_class, [Customer])
    name = str(uuid.uuid4())
    data = dict(name=name)
    response = requests.post(f"{live_server}{reverse('customer/create')}", data=data)
    response.raise_for_status()
    assert Customer.objects.filter(name=name).exists()

    # Assert model cannot be deleted
    audit_entry = model_class.objects.all().get()
    with pytest.raises(OperationalError, match=r"cannot delete from view"):
        audit_entry.delete()
