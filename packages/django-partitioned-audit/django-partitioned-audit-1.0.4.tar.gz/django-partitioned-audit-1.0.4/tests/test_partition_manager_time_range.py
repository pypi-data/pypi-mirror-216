from datetime import date
from typing import List
from typing import Union
from unittest.mock import Mock
from unittest.mock import PropertyMock
from unittest.mock import patch

import pytest

from django_partitioned_audit.audit_table.audit_table_manager import AuditTableManager
from django_partitioned_audit.partitions.partition_info import PartitionInfo
from django_partitioned_audit.partitions.partition_manager_time_range import PartitionManager
from django_partitioned_audit.partitions.time_range_partitioning import MonthlyTimeRangeGenerator


def test_generate_partition_info_for_current_period(audit_table_manager: AuditTableManager):
    pm = PartitionManager(time_range_generator=MonthlyTimeRangeGenerator())
    with patch.object(PartitionManager, "today", new_callable=PropertyMock) as mock:
        mock.return_value = date(1988, 3, 22)
        partition_info = pm.generate_partition_info_for_current_period()
        assert partition_info.partition == f"{audit_table_manager.partitioned_table_name}_19880301_19880401"

        mock.return_value = date(1988, 12, 22)
        partition_info = pm.generate_partition_info_for_current_period()
        assert partition_info.partition == f"{audit_table_manager.partitioned_table_name}_19881201_19890101"


def test_new_partition():
    pm = PartitionManager(time_range_generator=MonthlyTimeRangeGenerator())
    previous = PartitionInfo.create("part", date(1991, 1, 1), date(1991, 2, 1))

    assert pm.new_partition(previous) == PartitionInfo.create("part", date(1991, 2, 1), date(1991, 3, 1))


def test_new_partition_with_previous_starting_off_period():
    pm = PartitionManager(time_range_generator=MonthlyTimeRangeGenerator())
    assert pm.new_partition(PartitionInfo.create("part", date(1991, 1, 22), date(1991, 2, 1))) == PartitionInfo.create(
        "part", date(1991, 2, 1), date(1991, 3, 1)
    )


def test_new_partition_with_previous_ending_off_period():
    pm = PartitionManager(time_range_generator=MonthlyTimeRangeGenerator())
    assert pm.new_partition(PartitionInfo.create("part", date(1991, 1, 1), date(1991, 1, 20))) == PartitionInfo.create(
        "part", date(1991, 1, 20), date(1991, 2, 1)
    )

    assert pm.new_partition(PartitionInfo.create("part", date(1991, 1, 1), date(1991, 1, 31))) == PartitionInfo.create(
        "part", date(1991, 1, 31), date(1991, 2, 1)
    )


@pytest.mark.parametrize("params", [0, 1, 2, 30, [31], [32], [45], [55]])
def test_generate_plan_when_no_partition_exists(params: Union[int, List[int]], audit_table_manager: AuditTableManager):
    if isinstance(params, int):
        extra_days = params
        expected_partitions_to_create = [
            PartitionInfo.create(audit_table_manager.partitioned_table_name, date(1991, 3, 1), date(1991, 4, 1)),
        ]
    else:
        extra_days = params[0]
        expected_partitions_to_create = [
            PartitionInfo.create(audit_table_manager.partitioned_table_name, date(1991, 3, 1), date(1991, 4, 1)),
            PartitionInfo.create(audit_table_manager.partitioned_table_name, date(1991, 4, 1), date(1991, 5, 1)),
        ]

    pm = PartitionManager(extra_days=extra_days, time_range_generator=MonthlyTimeRangeGenerator())
    with patch.object(PartitionManager, "today", new_callable=PropertyMock) as mock_today:
        mock_today.return_value = date(1991, 3, 1)
        with patch.object(PartitionManager, "get_existing_partitions", new_callable=Mock) as mock_part:
            mock_part.return_value = []

            plan = pm.generate_plan()
            assert plan.existing_partitions == []
            assert plan.partitions_to_create == expected_partitions_to_create


@pytest.mark.parametrize("params", [0, 1, 2, 30, [31], [32], [45], [55]])
def test_generate_plan_when_partition_exists(params: Union[int, List[int]], audit_table_manager: AuditTableManager):
    if isinstance(params, int):
        extra_days = params
        expected_created = []
    else:
        extra_days = params[0]
        expected_created = [
            PartitionInfo.create(audit_table_manager.partitioned_table_name, date(1991, 4, 1), date(1991, 5, 1)),
        ]

    pm = PartitionManager(extra_days=extra_days, time_range_generator=MonthlyTimeRangeGenerator())
    with patch.object(PartitionManager, "today", new_callable=PropertyMock) as mock_today:
        mock_today.return_value = date(1991, 3, 1)
        with patch.object(PartitionManager, "get_existing_partitions", new_callable=Mock) as mock_part:
            mock_part.return_value = [
                PartitionInfo.create(audit_table_manager.partitioned_table_name, date(1991, 3, 1), date(1991, 4, 1)),
            ]

            plan = pm.generate_plan()
            assert plan.existing_partitions == [
                PartitionInfo.create(audit_table_manager.partitioned_table_name, date(1991, 3, 1), date(1991, 4, 1)),
            ]
            assert plan.partitions_to_create == expected_created


@pytest.mark.parametrize("params", [0, 1, 16, [17], [30]])
def test_generate_plan_when_partition_exists_but_not_for_current(
    params: Union[int, List[int]], audit_table_manager: AuditTableManager
):
    if isinstance(params, int):
        extra_days = params
        expected_created = [
            PartitionInfo.create(audit_table_manager.partitioned_table_name, date(1991, 3, 1), date(1991, 4, 1)),
        ]
    else:
        extra_days = params[0]
        expected_created = [
            PartitionInfo.create(audit_table_manager.partitioned_table_name, date(1991, 3, 1), date(1991, 4, 1)),
            PartitionInfo.create(audit_table_manager.partitioned_table_name, date(1991, 4, 1), date(1991, 5, 1)),
        ]

    pm = PartitionManager(extra_days=extra_days, time_range_generator=MonthlyTimeRangeGenerator())
    with patch.object(PartitionManager, "today", new_callable=PropertyMock) as mock_today:
        mock_today.return_value = date(1991, 3, 15)
        with patch.object(PartitionManager, "get_existing_partitions", new_callable=Mock) as mock_part:
            mock_part.return_value = [
                PartitionInfo.create(audit_table_manager.partitioned_table_name, date(1991, 2, 1), date(1991, 3, 1)),
            ]

            plan = pm.generate_plan()
            assert plan.existing_partitions == [
                PartitionInfo.create(audit_table_manager.partitioned_table_name, date(1991, 2, 1), date(1991, 3, 1)),
            ]
            assert plan.partitions_to_create == expected_created
