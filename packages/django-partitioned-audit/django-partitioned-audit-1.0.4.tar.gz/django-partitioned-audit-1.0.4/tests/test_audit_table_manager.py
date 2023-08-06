from uuid import uuid4

import pytest
from app.models import Customer
from django.db import IntegrityError
from django.db import connection
from django.db import transaction

from django_partitioned_audit.audit_table.advanced_audit_table_manager import AdvancedAuditTableManager
from django_partitioned_audit.audit_table.audit_table_manager import AuditTableManager
from django_partitioned_audit.audit_table.simple_audit_table_manager import SimpleAuditTableManager
from django_partitioned_audit.models import AdvancedAuditEntry
from django_partitioned_audit.models import SimpleAuditEntry
from django_partitioned_audit.partitions.partition_manager_time_range import PartitionManager
from django_partitioned_audit.partitions.time_range_partitioning import DailyTimeRangeGenerator

# pylint: skip-file


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize(
    "audit_table_manager_class,model_class",
    [[SimpleAuditTableManager, SimpleAuditEntry], [AdvancedAuditTableManager, AdvancedAuditEntry]],
)
def test_audit_table_manager(audit_table_manager_class, model_class, settings_audit_table_manager, remove_auditing):
    # TODO: we're testing too much here, need to refactor and split this in many tests
    settings_audit_table_manager(audit_table_manager_class)
    audit_manager = AuditTableManager.get_implementation()
    assert isinstance(audit_manager, audit_table_manager_class)

    customer_count = 0

    # >>> let's create an instance without auditing, it should work
    assert Customer.objects.all().count() == customer_count
    Customer.objects.create(name=str(uuid4()))  # make sure model without auditing works
    customer_count += 1
    assert Customer.objects.all().count() == customer_count

    # >>> create partitioned table
    pm = PartitionManager(audit_manager=audit_manager, time_range_generator=DailyTimeRangeGenerator())
    assert audit_manager.partitioned_table_name not in pm.get_tables()
    with connection.cursor() as cursor:
        audit_manager.create_partitioned_table(cursor)
    assert audit_manager.partitioned_table_name in pm.get_tables()

    # >>> let's create an instance without auditing, it should work
    Customer.objects.create(name=str(uuid4()))  # make sure model without auditing works
    customer_count += 1
    assert Customer.objects.all().count() == customer_count

    # >>> enable auditing
    with connection.cursor() as cursor:
        audit_manager.enable_audit_for_table(cursor, Customer._meta.db_table)

    # >>> partitioned table exists, but no partitions... insert should fail
    with transaction.atomic():
        with pytest.raises(IntegrityError, match=r"no partition of relation .* found for row"):
            Customer.objects.create(name=str(uuid4()))

    # >>> let's create the partition
    pi = pm.generate_partition_info_for_current_period()
    sql, params = audit_manager.generate_create_partition(pi.partition, pi.partitioned_table, pi.from_date, pi.to_date)
    with connection.cursor() as cursor:
        cursor.execute(sql, params)

    # >>> let's create a model & test audit entries
    assert model_class.objects.all().count() == 0
    customer = Customer.objects.create(name=str(uuid4()))
    customer_count += 1
    assert Customer.objects.all().count() == customer_count
    assert model_class.objects.all().count() == 1
    customer.name = str(uuid4())
    customer.save()
    assert model_class.objects.all().count() == 2
