from datetime import date
from typing import List
from typing import Tuple
from typing import Type

from django.db.models import Model

from django_partitioned_audit.audit_table.audit_table_manager import AuditTableManager


class DummyAuditTableManager(AuditTableManager):
    def __init__(self, partitioned_table_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.custom_partitioned_table_name = partitioned_table_name

    @property
    def partitioned_table_name(self) -> str:
        return self.custom_partitioned_table_name

    @property
    def model(self) -> Type[Model]:
        pass

    def create_partitioned_table(self, cursor):
        pass

    def enable_audit_for_table(self, cursor, table_name: str):
        pass

    def disable_audit_for_table(self, cursor, table_name: str):
        pass

    def drop_all(self, cursor):
        pass

    def generate_create_partition(
        self, partition_name: str, partitioned_table: str, from_date: date, to_date: date
    ) -> Tuple[str, List[object]]:
        pass
