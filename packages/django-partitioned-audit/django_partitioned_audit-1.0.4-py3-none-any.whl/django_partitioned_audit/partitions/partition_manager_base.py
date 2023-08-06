import datetime
from typing import Iterator
from typing import List

from django.db import connection

from django_partitioned_audit.audit_table.audit_table_manager import AuditTableManager
from django_partitioned_audit.partitions.partition_info import PartitionInfo
from django_partitioned_audit.partitions.time_range_partitioning import TimeRangeGenerator


class BasePartitionManager:
    default_extra_days = 30
    postgresql_table_name_limit = 63
    partition_suffix_len = 18

    def __init__(
        self,
        time_range_generator: TimeRangeGenerator,
        extra_days=default_extra_days,
        audit_manager: AuditTableManager = None,
    ):
        self._now = datetime.datetime.now()
        self._time_range_generator = time_range_generator
        self._extra_days = extra_days
        self._audit_manager = audit_manager or AuditTableManager.get_implementation()

        assert self._extra_days >= 0
        self._validate_partitioned_table()

    @property
    def audit_manager(self) -> AuditTableManager:
        return self._audit_manager

    @property
    def _partitioned_table(self):
        return self._audit_manager.partitioned_table_name

    def _validate_partitioned_table(self):
        if len(self._partitioned_table) > (self.postgresql_table_name_limit - self.partition_suffix_len):
            raise ValueError("partitioned_table is too long, partitions will be truncated")

    @property
    def today(self) -> datetime.date:
        return self._now.date()

    def get_tables(self) -> List[str]:
        """Return the name of all the tables"""
        with connection.cursor() as cursor:
            # https://www.postgresql.org/docs/current/infoschema-tables.html
            cursor.execute(
                """
                SELECT table_name
                    FROM information_schema.tables
                    ORDER BY table_name""",
            )
            tables = [row[0] for row in cursor.fetchall()]
            return tables

    def get_existing_partitions(self, include_other: bool = False) -> Iterator[PartitionInfo]:
        """Return information about existing partitions"""
        for table_name in self.get_tables():
            partition_info = PartitionInfo.parse(table_name)
            if partition_info:
                if include_other:
                    yield partition_info
                else:
                    if partition_info.partitioned_table == self._partitioned_table:
                        yield partition_info

    def create_partitions(self, partitions: List[PartitionInfo]):
        assert partitions
        assert {pi.partitioned_table for pi in partitions} == {self._partitioned_table}

        tables = self.get_tables()
        if self._partitioned_table not in tables:
            raise ValueError(f"Partitioned table '{self._partitioned_table}' not found. Tables: {sorted(tables)}")

        with connection.cursor() as cursor:
            for part_info in partitions:
                sql, params = part_info.generate_create_partition()
                cursor.execute(sql, params)
