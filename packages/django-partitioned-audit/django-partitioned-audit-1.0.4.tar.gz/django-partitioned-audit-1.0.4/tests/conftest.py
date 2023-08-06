import datetime
import os
import uuid
from datetime import timedelta
from typing import Callable
from typing import List

import pytest
from django.db import connection

from django_partitioned_audit.audit_table.advanced_audit_table_manager import AdvancedAuditTableManager
from django_partitioned_audit.audit_table.audit_table_manager import AuditTableManager
from django_partitioned_audit.audit_table.simple_audit_table_manager import SimpleAuditTableManager
from django_partitioned_audit.partitions.partition_info import PartitionInfo
from django_partitioned_audit.partitions.partition_manager_time_range import PartitionManager
from django_partitioned_audit.partitions.time_range_partitioning import DailyTimeRangeGenerator
from django_partitioned_audit.partitions.time_range_partitioning import MonthlyTimeRangeGenerator

ADVANCED_FQCN = "django_partitioned_audit.audit_table.advanced_audit_table_manager.AdvancedAuditTableManager"

skipifadvanced = pytest.mark.skipif(
    os.environ.get("DPA_AUDIT_TABLE_MANAGER") == ADVANCED_FQCN,
    reason="skip when testing AdvancedAuditTableManager",
)


@pytest.fixture
def partition_created() -> PartitionInfo:
    """
    Creates a partition for current time, so test can run and audit events inserted.
    We need this because if only the `partitioned table` is created in migration, but no partitions.
    """
    today = datetime.date.today()
    audit_tm = AuditTableManager.get_implementation()
    default_partitioned_table = audit_tm.partitioned_table_name
    info = PartitionInfo.create(default_partitioned_table, today, today + timedelta(days=2))
    sql, params = info.generate_create_partition()
    with connection.cursor() as cursor:
        cursor.execute(sql, params)

    yield info

    with connection.cursor() as cursor:
        # Why we need to delete the partition? :/
        cursor.execute(f"DROP TABLE {info.partition}")


@pytest.fixture
def partitioned_table_create():
    def func(partitioned_table):
        with connection.cursor() as cursor:
            sql = f"""
            CREATE TABLE {partitioned_table} (
                column_1 TEXT NULL,
                column_2 TEXT NULL,
                creation_timestamp timestamp with time zone DEFAULT now() NOT NULL
            ) PARTITION BY RANGE (creation_timestamp);
            """
            cursor.execute(sql)

    return func


@pytest.fixture
def very_long_named_partitioned_table(partitioned_table_create: Callable):
    """
    Creates a `partitioned table` with a name that is truncated by postgres.
    Thus, `partitions` will be truncated too.
    """
    partitioned_table = f"partitioned_table_{uuid.uuid4().hex}_long_name_lorem_ipsum_dolor_sit_amet_consectetur"
    assert len(partitioned_table) == 99, partitioned_table

    partitioned_table_create(partitioned_table)

    return partitioned_table


@pytest.fixture
def partitioned_table(partitioned_table_create: Callable):
    """
    Creates a `partitioned table` with a name that is short,
    guaranteeing that names of `partitions` won't be truncated.
    """
    partitioned_table = f"partitioned_table_{uuid.uuid4().hex[0:7]}"
    assert len(partitioned_table) == 25
    partitioned_table_create(partitioned_table)
    return partitioned_table


@pytest.fixture
def truncate_partitions():
    pm = PartitionManager(time_range_generator=MonthlyTimeRangeGenerator())
    with connection.cursor() as cursor:
        for info in pm.get_existing_partitions():
            cursor.execute(f"TRUNCATE {info.partition}")

    yield

    with connection.cursor() as cursor:
        for info in pm.get_existing_partitions():
            cursor.execute(f"DROP TABLE {info.partition}")


@pytest.fixture()
def audit_table_manager() -> AuditTableManager:
    return AuditTableManager.get_implementation()


@pytest.fixture
def settings_audit_table_manager(settings):
    def func(clazz):
        fqcn = f"{clazz.__module__}.{clazz.__qualname__}"
        settings.DPA_AUDIT_TABLE_MANAGER = fqcn

    return func


@pytest.fixture
def remove_auditing(post_test_disable_trigger):
    for am in [SimpleAuditTableManager(), AdvancedAuditTableManager()]:
        with connection.cursor() as cursor:
            am.drop_all(cursor)
        tmp = PartitionManager(audit_manager=am, time_range_generator=DailyTimeRangeGenerator())
        assert not list(tmp.get_existing_partitions())
        assert am.partitioned_table_name not in list(tmp.get_tables())

    yield


@pytest.fixture
def post_test_disable_trigger():
    yield

    # After each test the tables are truncated, but if this operation is audited after the partition
    # is deleted, the truncate() made by Django/pytest fails. Here we're doing a trick to avoid that failure.
    # Seems like this is not needed when test are successful :/ but let's do it just in case
    # TODO: this breaks encapsulation of `AuditTableManager`, maybe should be refactored
    with connection.cursor() as cursor:
        sql = """
        CREATE OR REPLACE FUNCTION if_modified_func() RETURNS TRIGGER AS $body$
        BEGIN
            RETURN NULL;
        END;
        $body$
        LANGUAGE plpgsql
        """
        cursor.execute(sql)

        sql = """
        CREATE OR REPLACE FUNCTION trigger_audit_entry_creator_func_v2() RETURNS TRIGGER AS $body$
        BEGIN
            RETURN NULL;
        END;
        $body$
        LANGUAGE plpgsql
        """
        cursor.execute(sql)


@pytest.fixture
def use_audit_table_manager(settings, remove_auditing):
    def func(audit_table_manager_class, enable_models: List):
        clazz = f"{audit_table_manager_class.__module__}.{audit_table_manager_class.__qualname__}"
        settings.DPA_AUDIT_TABLE_MANAGER = clazz

        audit_manager = AuditTableManager.get_implementation()
        assert isinstance(audit_manager, audit_table_manager_class)
        with connection.cursor() as cursor:
            audit_manager.create_partitioned_table(cursor)
            for a_model in enable_models:
                audit_manager.enable_audit_for_table(cursor, a_model._meta.db_table)

        today = datetime.date.today()
        audit_tm = AuditTableManager.get_implementation()
        default_partitioned_table = audit_tm.partitioned_table_name
        info = PartitionInfo.create(default_partitioned_table, today, today + timedelta(days=2))
        sql, params = info.generate_create_partition()
        with connection.cursor() as cursor:
            cursor.execute(sql, params)

    return func


# def _table_exists(table_name: str) -> bool:
#     with transaction.atomic():
#         with connection.cursor() as cursor:
#             try:
#                 cursor.execute(f"select * from {table_name} limit 1")
#             except ProgrammingError as err:
#                 if re.search(rf"relation.*{table_name}.*does not exist", err.args[0].splitlines()[0]):
#                     return False
#                 else:
#                     raise
#             return True
