from uuid import uuid4

import pytest
from app import models as models_first_app
from django.db import IntegrityError
from django.db import ProgrammingError
from django.db import transaction
from second_app import models as models_second_app

from django_partitioned_audit.audit_table.audit_table_manager import AuditTableManager

# pylint: skip-file


@pytest.mark.django_db(transaction=True)
def test_without_auditing(truncate_partitions, remove_auditing):
    ModelClass = AuditTableManager.get_implementation().model  # noqa

    customer_first_app = models_first_app.Customer.objects.create(pk=4321, name=str(uuid4()))
    customer_second_app = models_second_app.Customer.objects.create(pk=4321, name=str(uuid4()))

    with pytest.raises(IntegrityError):
        # inserting again with same PK should fail
        models_first_app.Customer.objects.create(pk=4321, name=str(uuid4()))

    with pytest.raises(IntegrityError):
        # inserting again with same PK should fail
        models_second_app.Customer.objects.create(pk=4321, name=str(uuid4()))

    assert models_first_app.Customer.objects.filter(name=customer_first_app.name).get().pk == 4321
    assert models_second_app.Customer.objects.filter(name=customer_second_app.name).get().pk == 4321

    with transaction.atomic():
        with pytest.raises(ProgrammingError, match=r"relation .* does not exist"):
            ModelClass.objects.filter_model(models_first_app.Customer).count()


@pytest.mark.django_db(transaction=True)
def test_audit_two_app_with_same_model_names(partition_created, post_test_disable_trigger):
    ModelClass = AuditTableManager.get_implementation().model  # noqa

    assert ModelClass.objects.filter_model(models_first_app.Customer).count() == 0
    assert ModelClass.objects.filter_model(models_second_app.Customer).count() == 0

    customer_first_app = models_first_app.Customer.objects.create(pk=4321, name=str(uuid4()))
    assert ModelClass.objects.filter_model(models_first_app.Customer).count() == 1
    assert ModelClass.objects.filter_model(models_second_app.Customer).count() == 0

    customer_second_app = models_second_app.Customer.objects.create(pk=4321, name=str(uuid4()))
    assert ModelClass.objects.filter_model(models_first_app.Customer).count() == 1
    assert ModelClass.objects.filter_model(models_second_app.Customer).count() == 1

    audit = ModelClass.objects.filter_model(models_first_app.Customer).get()
    assert audit.get_row_data()["name"] == customer_first_app.name

    audit = ModelClass.objects.filter_model(models_second_app.Customer).get()
    assert audit.get_row_data()["name"] == customer_second_app.name
