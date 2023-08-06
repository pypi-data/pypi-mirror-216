import uuid

import pytest
from app.models import Customer
from app.models import Invoice
from app.models import Product

from django_partitioned_audit.audit_table.advanced_audit_table_manager import AdvancedAuditTableManager
from django_partitioned_audit.models import AdvancedAuditEntry
from django_partitioned_audit.models import Operation
from django_partitioned_audit.models import SimpleAuditEntry
from tests.conftest import skipifadvanced

# pylint: skip-file


@skipifadvanced
@pytest.mark.django_db(transaction=True)
def test_filter_model(partition_created):
    initial_name = str(uuid.uuid4())
    new_name = str(uuid.uuid4())

    assert SimpleAuditEntry.objects.filter_model(Invoice).count() == 0
    assert SimpleAuditEntry.objects.filter_model(Product).count() == 0
    assert SimpleAuditEntry.objects.filter_model(Customer).count() == 0

    Invoice.objects.create(name=str(uuid.uuid4()))
    Product.objects.create(name=str(uuid.uuid4()))
    Product.objects.create(name=str(uuid.uuid4()))
    Customer.objects.create(name=str(uuid.uuid4()))
    Customer.objects.create(name=str(uuid.uuid4()))
    customer = Customer.objects.create(name=initial_name)

    assert SimpleAuditEntry.objects.filter_model(Invoice).count() == 1
    assert SimpleAuditEntry.objects.filter_model(Product).count() == 2
    assert SimpleAuditEntry.objects.filter_model(Customer).count() == 3

    customer.name = new_name
    customer.save()

    assert SimpleAuditEntry.objects.filter_model(Customer).count() == 4


@skipifadvanced
@pytest.mark.django_db(transaction=True)
def test_filter_payload(partition_created):
    Customer.objects.create(name=str(uuid.uuid4()))
    Customer.objects.create(name=str(uuid.uuid4()))

    initial_name = str(uuid.uuid4())
    new_name = str(uuid.uuid4())
    customer = Customer.objects.create(name=initial_name)

    assert SimpleAuditEntry.objects.filter_payload(name=initial_name).count() == 1
    assert SimpleAuditEntry.objects.filter_payload(name=new_name).count() == 0

    customer.active = False
    customer.save()

    assert SimpleAuditEntry.objects.filter_payload(name=initial_name).count() == 2
    assert SimpleAuditEntry.objects.filter_payload(name=new_name).count() == 0

    customer.name = new_name
    customer.save()

    assert SimpleAuditEntry.objects.filter_payload(name=initial_name).count() == 2
    assert SimpleAuditEntry.objects.filter_payload(name=new_name).count() == 1


@skipifadvanced
@pytest.mark.django_db(transaction=True)
def test_filter_by_primary_key(partition_created):
    Invoice.objects.create(name=str(uuid.uuid4()))
    Product.objects.create(name=str(uuid.uuid4()))
    Customer.objects.create(name=str(uuid.uuid4()))

    invoice = Invoice.objects.create(name=str(uuid.uuid4()))
    product = Product.objects.create(name=str(uuid.uuid4()))
    customer = Customer.objects.create(name=str(uuid.uuid4()))

    audit_entry = SimpleAuditEntry.objects.filter_model(Invoice).filter_payload(id=str(invoice.pk)).get()
    assert audit_entry.get_row_data()["name"] == invoice.name

    audit_entry = SimpleAuditEntry.objects.filter_model(Product).filter_payload(product_id=int(product.pk)).get()
    assert audit_entry.get_row_data()["name"] == product.name

    audit_entry = SimpleAuditEntry.objects.filter_model(Customer).filter_payload(id=int(customer.pk)).get()
    assert audit_entry.get_row_data()["name"] == customer.name


@skipifadvanced
@pytest.mark.django_db(transaction=True)
def test_filter_by_primary_key_advanced(use_audit_table_manager):
    use_audit_table_manager(AdvancedAuditTableManager, [Invoice, Product, Customer])

    Invoice.objects.create(name=str(uuid.uuid4()))
    Product.objects.create(name=str(uuid.uuid4()))
    Customer.objects.create(name=str(uuid.uuid4()))

    invoice = Invoice.objects.create(name=str(uuid.uuid4()))
    product = Product.objects.create(name=str(uuid.uuid4()))
    customer = Customer.objects.create(name=str(uuid.uuid4()))

    audit_entry = AdvancedAuditEntry.objects.filter_model(Invoice).filter_payload(id=str(invoice.pk)).get()
    assert audit_entry.get_row_data()["name"] == invoice.name

    audit_entry = AdvancedAuditEntry.objects.filter_model(Product).filter_payload(product_id=str(product.pk)).get()
    assert audit_entry.get_row_data()["name"] == product.name
    # Pay attention at `filter_payload()`... For `AdvancedAuditEntry` we use `str(product.pk)`,
    # because even tough JSONB supports non-str, in the table we're using HSTORE

    audit_entry = AdvancedAuditEntry.objects.filter_model(Customer).filter_payload(id=str(customer.pk)).get()
    assert audit_entry.get_row_data()["name"] == customer.name
    # The same here with `filter_payload(id=str(customer.pk))`


@skipifadvanced
@pytest.mark.django_db(transaction=True)
def test_filter_operation(partition_created):
    assert SimpleAuditEntry.objects.filter_model(Invoice).count() == 0
    assert SimpleAuditEntry.objects.filter_model(Product).count() == 0
    assert SimpleAuditEntry.objects.filter_model(Customer).count() == 0

    Invoice.objects.create(name=str(uuid.uuid4()))
    product = Product.objects.create(name=str(uuid.uuid4()))
    customer = Customer.objects.create(name=str(uuid.uuid4()))

    customer.name = str(uuid.uuid4())
    customer.save()

    product.delete()

    assert SimpleAuditEntry.objects.filter_model(Invoice).count() == 1
    assert SimpleAuditEntry.objects.filter_model(Product).count() == 2
    assert SimpleAuditEntry.objects.filter_model(Customer).count() == 2

    assert SimpleAuditEntry.objects.filter_operation(Operation.INSERT).count() == 3
    assert SimpleAuditEntry.objects.filter_operation(Operation.UPDATE).count() == 1
    assert SimpleAuditEntry.objects.filter_operation(Operation.DELETE).count() == 1

    tables = SimpleAuditEntry.objects.filter_operation(Operation.INSERT).values_list("object_table", flat=True)
    assert set(tables) == {"app_customer", "app_invoice", "app_product"}

    tables = SimpleAuditEntry.objects.filter_operation(Operation.UPDATE).values_list("object_table", flat=True)
    assert set(tables) == {"app_customer"}

    tables = SimpleAuditEntry.objects.filter_operation(Operation.DELETE).values_list("object_table", flat=True)
    assert set(tables) == {"app_product"}
