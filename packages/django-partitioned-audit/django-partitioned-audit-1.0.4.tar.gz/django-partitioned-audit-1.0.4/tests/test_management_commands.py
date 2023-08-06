import re
from datetime import date
from io import StringIO
from typing import List
from unittest.mock import Mock
from unittest.mock import PropertyMock
from unittest.mock import patch

import pytest
from django.core import management

from django_partitioned_audit.audit_table.audit_table_manager import AuditTableManager
from django_partitioned_audit.partitions.partition_manager_time_range import PartitionManager

# pylint: skip-file


@pytest.mark.django_db(transaction=True)
def test_flush():
    management.call_command("flush", verbosity=0, interactive=False)


@pytest.mark.django_db(transaction=True)
def test_migrate():
    management.call_command("migrate", verbosity=0, interactive=False)


@pytest.mark.django_db(transaction=True)
def test_manage_partition_tables_create_monthly(truncate_partitions, audit_table_manager: AuditTableManager):
    partitioned_table = audit_table_manager.partitioned_table_name
    with patch.object(PartitionManager, "get_existing_partitions", new_callable=Mock) as mock_partitions:
        with patch.object(PartitionManager, "today", new_callable=PropertyMock) as mock_today:
            mock_partitions.return_value = []
            mock_today.return_value = date(1877, 3, 22)
            out = StringIO()
            management.call_command("manage_partition_tables", "create", verbosity=0, stdout=out)
            lines: List[str] = out.getvalue().splitlines()
            assert lines

            lines_tables = [_ for _ in lines if re.search(rf"{partitioned_table}.*to create", _)]
            assert len(lines_tables) == 2
            assert any([re.search(rf"{partitioned_table}_18770301_18770401.*to create", _) for _ in lines_tables])
            assert any([re.search(rf"{partitioned_table}_18770401_18770501.*to create", _) for _ in lines_tables])


@pytest.mark.django_db(transaction=True)
def test_manage_partition_tables_create_weekly(truncate_partitions, audit_table_manager: AuditTableManager):
    partitioned_table = audit_table_manager.partitioned_table_name

    with patch.object(PartitionManager, "today", new_callable=PropertyMock) as mock_today:
        mock_today.return_value = date(1877, 3, 22)

        out = StringIO()
        management.call_command(
            "manage_partition_tables",
            "create",
            "--time-range-generator=WeeklyTimeRangeGenerator",
            verbosity=0,
            stdout=out,
        )
        lines: List[str] = out.getvalue().splitlines()
        assert lines

        lines_tables = [_ for _ in lines if re.search(rf"{partitioned_table}.*to create", _)]
        assert len(lines_tables) == 5
        assert any([re.search(rf"{partitioned_table}_18770322_18770329.*to create", _) for _ in lines_tables])
        assert any([re.search(rf"{partitioned_table}_18770329_18770405.*to create", _) for _ in lines_tables])
        assert any([re.search(rf"{partitioned_table}_18770405_18770412.*to create", _) for _ in lines_tables])
        assert any([re.search(rf"{partitioned_table}_18770412_18770419.*to create", _) for _ in lines_tables])
        assert any([re.search(rf"{partitioned_table}_18770419_18770426.*to create", _) for _ in lines_tables])


@pytest.mark.django_db(transaction=True)
def test_manage_partition_tables_create_daily(truncate_partitions, audit_table_manager: AuditTableManager):
    partitioned_table = audit_table_manager.partitioned_table_name

    with patch.object(PartitionManager, "today", new_callable=PropertyMock) as mock_today:
        mock_today.return_value = date(1877, 3, 22)

        out = StringIO()
        management.call_command(
            "manage_partition_tables",
            "create",
            "--time-range-generator=DailyTimeRangeGenerator",
            "--extra-days=6",
            verbosity=0,
            stdout=out,
        )
        lines: List[str] = out.getvalue().splitlines()
        assert lines

        lines_tables = [_ for _ in lines if re.search(rf"{partitioned_table}.*to create", _)]
        assert len(lines_tables) == 7
        assert any([re.search(rf"{partitioned_table}_18770322_18770323.*to create", _) for _ in lines_tables])
        assert any([re.search(rf"{partitioned_table}_18770323_18770324.*to create", _) for _ in lines_tables])
        assert any([re.search(rf"{partitioned_table}_18770324_18770325.*to create", _) for _ in lines_tables])
        assert any([re.search(rf"{partitioned_table}_18770325_18770326.*to create", _) for _ in lines_tables])
        assert any([re.search(rf"{partitioned_table}_18770326_18770327.*to create", _) for _ in lines_tables])
        assert any([re.search(rf"{partitioned_table}_18770327_18770328.*to create", _) for _ in lines_tables])
        assert any([re.search(rf"{partitioned_table}_18770328_18770329.*to create", _) for _ in lines_tables])


@pytest.mark.django_db(transaction=True)
def test_manage_partition_tables_create_twice(truncate_partitions, audit_table_manager: AuditTableManager):
    partitioned_table = audit_table_manager.partitioned_table_name

    with patch.object(PartitionManager, "today", new_callable=PropertyMock) as mock_today:
        mock_today.return_value = date(1877, 3, 22)

        out = StringIO()
        management.call_command("manage_partition_tables", "create", verbosity=0, stdout=out)
        lines: List[str] = out.getvalue().splitlines()
        assert lines

        lines_tables = [_ for _ in lines if re.search(rf"{partitioned_table}.*to create", _)]
        assert len(lines_tables) == 2
        assert any([re.search(rf"{partitioned_table}_18770301_18770401.*to create", _) for _ in lines_tables])
        assert any([re.search(rf"{partitioned_table}_18770401_18770501.*to create", _) for _ in lines_tables])

        out = StringIO()
        management.call_command("manage_partition_tables", "create", verbosity=0, stdout=out)
        lines: List[str] = out.getvalue().splitlines()
        assert lines

        lines_tables = [_ for _ in lines if re.search(rf"{partitioned_table}.*to create", _)]
        assert len(lines_tables) == 0

        lines_tables = [_ for _ in lines if re.search(rf"{partitioned_table}.*exists", _)]
        assert len(lines_tables) == 2
        assert any([re.search(rf"{partitioned_table}_18770301_18770401.*exists", _) for _ in lines_tables])
        assert any([re.search(rf"{partitioned_table}_18770401_18770501.*exists", _) for _ in lines_tables])
