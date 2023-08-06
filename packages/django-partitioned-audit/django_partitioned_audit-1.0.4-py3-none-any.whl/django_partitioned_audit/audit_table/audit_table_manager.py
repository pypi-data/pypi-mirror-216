import abc
from datetime import date
from typing import List
from typing import Tuple
from typing import Type
from typing import TypeVar

from django.conf import settings
from django.db.models import Model
from django.utils.module_loading import import_string

SelfAuditTableManager = TypeVar("SelfAuditTableManager", bound="AuditTableManager")


DEFAULT_IMPL = "django_partitioned_audit.audit_table.simple_audit_table_manager.SimpleAuditTableManager"


class AuditTableManager(abc.ABC):
    @property
    @abc.abstractmethod
    def partitioned_table_name(self) -> str:
        ...

    @property
    @abc.abstractmethod
    def model(self) -> Type[Model]:
        ...

    @abc.abstractmethod
    def create_partitioned_table(self, cursor):
        ...

    @abc.abstractmethod
    def enable_audit_for_table(self, cursor, table_name: str):
        ...

    @abc.abstractmethod
    def disable_audit_for_table(self, cursor, table_name: str):
        ...

    @abc.abstractmethod
    def generate_create_partition(
        self, partition_name: str, partitioned_table: str, from_date: date, to_date: date
    ) -> Tuple[str, List[object]]:
        ...

    @abc.abstractmethod
    def drop_all(self, cursor):
        ...

    @classmethod
    def get_implementation(cls) -> SelfAuditTableManager:
        try:
            impl_class_name = settings.DPA_AUDIT_TABLE_MANAGER
        except AttributeError:
            impl_class_name = DEFAULT_IMPL
        impl_class: Type[SelfAuditTableManager] = import_string(impl_class_name)
        return impl_class()

    def get_triggers(self, cursor) -> List[List[str]]:
        """Return the name of all triggers"""
        # https://www.postgresql.org/docs/current/infoschema-tables.html
        cursor.execute("SELECT event_object_table, trigger_name FROM information_schema.triggers")
        table_trigger_list = [[row[0], row[1]] for row in cursor.fetchall()]
        return table_trigger_list
