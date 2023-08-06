import enum
import logging
from typing import Type

from django.contrib.postgres.fields import HStoreField
from django.db import models
from django.db.models import Model
from django.db.models import Q

import django_partitioned_audit.signals  # noqa pylint: disable=unused-import

logger = logging.getLogger(__name__)


class Operation(enum.Enum):
    INSERT = 1
    UPDATE = 2
    DELETE = 3
    TRUNCATE = 4


# ----------------------------------------------------------------------------------------------------
# SimpleAuditTableManager
# ----------------------------------------------------------------------------------------------------


class SimpleAuditEntryQuerySet(models.QuerySet):
    def filter_model(self, model_class: Type[Model]):
        """Filter audit events by the model that generated the events"""
        return self.filter(object_table__iexact=model_class._meta.db_table)  # noqa

    def filter_payload(self, **kwargs):
        """
        Filter audit events by a value in the `payload` of the audit event, that means,
        the value of the column at the time the audit even was generated.
        """
        assert kwargs
        filter_kwargs = {}
        for key_name, key_value in kwargs.items():
            filter_kwargs[f"object_payload__{key_name}"] = key_value

        return self.filter(**filter_kwargs)

    def filter_operation(self, operation: Operation):
        if operation == Operation.INSERT:
            return self.filter(audit_operation="I")
        elif operation == Operation.UPDATE:
            return self.filter(audit_operation="U")
        elif operation == Operation.DELETE:
            return self.filter(audit_operation="D")
        elif operation == Operation.TRUNCATE:
            raise NotImplementedError("TRUNCATE is not supported by this implementation")
        else:
            raise ValueError(f"Invalid operation: {operation}")


class SimpleAuditEntry(Model):
    """
    This model exists to facilitate reading audit events.
    This is mapped to the view.
    No update or delete operations can be done.
    """

    object_table = models.CharField(max_length=63)
    object_payload = models.JSONField()

    audit_entry_created = models.DateTimeField()
    audit_entry_created_statement_timestamp = models.DateTimeField()
    audit_txid_current = models.BigIntegerField()
    audit_operation = models.CharField(max_length=32)

    objects = SimpleAuditEntryQuerySet.as_manager()

    class Meta:
        managed = False
        db_table = "audit_simple_view"

    def __str__(self):
        return f"{self.__class__.__name__} " f"{self.object_table} " f"{self.audit_operation}"

    def is_insert(self):
        return self.audit_operation == "I"

    def is_update(self):
        return self.audit_operation == "U"

    def is_delete(self):
        return self.audit_operation == "D"

    def get_row_data(self) -> dict:
        return self.object_payload


# ----------------------------------------------------------------------------------------------------
# AdvancedAuditTableManager
# ----------------------------------------------------------------------------------------------------


class AdvancedAuditEntryQuerySet(models.QuerySet):
    def filter_model(self, model_class: Type[Model]):
        """Filter audit events by the model that generated the events"""
        return self.filter(table_name__iexact=model_class._meta.db_table)  # noqa

    def filter_payload(self, **kwargs):
        assert kwargs
        qs = self
        for key_name, key_value in kwargs.items():
            filter_kwargs_1 = {
                f"changed_fields_json__{key_name}": key_value,
            }
            filter_kwargs_2 = {
                f"changed_fields_json__{key_name}__isnull": True,
                f"row_data_json__{key_name}": key_value,
            }
            qs = qs.filter(Q(**filter_kwargs_1) | Q(**filter_kwargs_2))

        return qs

    def filter_operation(self, operation: Operation):
        if operation == Operation.INSERT:
            return self.filter(action="I")
        elif operation == Operation.UPDATE:
            return self.filter(action="U")
        elif operation == Operation.DELETE:
            return self.filter(action="D")
        elif operation == Operation.TRUNCATE:
            return self.filter(action="T")
        else:
            raise ValueError(f"Invalid operation: {operation}")


class AdvancedAuditEntry(Model):
    event_id = models.BigAutoField(primary_key=True, help_text="Unique identifier for each auditable event")
    schema_name = models.TextField(help_text="Database schema audited table for this event is in")
    table_name = models.TextField(help_text="Non-schema-qualified table name of table event occured in")
    action_tstamp_tx = models.DateTimeField(
        help_text="Transaction start timestamp for tx in which audited event occurred"
    )
    action_tstamp_stm = models.DateTimeField(
        help_text="Statement start timestamp for tx in which audited event occurred"
    )
    action_tstamp_clk = models.DateTimeField(
        help_text="Wall clock time at which audited event''s trigger call occurred"
    )
    transaction_id = models.BigIntegerField(
        help_text="Identifier of transaction that made the change. May wrap, but unique paired with action_tstamp_tx."
    )
    action = models.CharField(max_length=1, help_text="Action type; I = insert, D = delete, U = update, T = truncate")
    row_data = HStoreField(
        help_text="Record value. Null for statement-level trigger. For INSERT this is the new tuple. "
        "For DELETE and UPDATE it is the old tuple."
    )
    changed_fields = HStoreField(
        help_text="New values of fields changed by UPDATE. Null except for row-level UPDATE events."
    )

    # relid IS 'Table OID. Changes with drop/create. Get with ''tablename''::regclass';
    # session_user_name IS 'Login / session user whose statement caused the audited event';
    # client_addr IS 'IP address of client that issued query. Null for unix domain socket.';
    # client_port IS 'Remote peer IP port address of client that issued query. Undefined for unix socket.';
    # client_query IS 'Top-level query that caused this auditable event. May be more than one statement.';
    # application_name IS 'Application name set when this audit event occurred. Can be changed in-session by client.';
    # statement_only IS '''t'' if audit event is from an FOR EACH STATEMENT trigger, ''f'' for FOR EACH ROW';

    row_data_json = models.JSONField(
        help_text="Record value. Null for statement-level trigger. For INSERT this is the new tuple. "
        "For DELETE and UPDATE it is the old tuple."
    )

    changed_fields_json = models.JSONField(
        help_text="New values of fields changed by UPDATE. Null except for row-level UPDATE events."
    )

    objects = AdvancedAuditEntryQuerySet.as_manager()

    class Meta:
        managed = False
        db_table = "logged_actions_view"

    def __str__(self):
        return f"{self.__class__.__name__} " f"{self.table_name} " f"{self.action}"

    def is_insert(self):
        return self.action == "I"

    def is_update(self):
        return self.action == "U"

    def is_delete(self):
        return self.action == "D"

    def is_truncate(self):
        return self.action == "T"

    def get_row_data(self) -> dict:
        row_data = {}
        row_data.update(self.row_data_json or {})
        row_data.update(self.changed_fields_json or {})
        return row_data
