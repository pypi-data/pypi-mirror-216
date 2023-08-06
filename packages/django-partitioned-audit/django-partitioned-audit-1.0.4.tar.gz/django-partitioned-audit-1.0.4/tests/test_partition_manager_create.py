from datetime import date
from typing import Callable
from unittest.mock import Mock
from unittest.mock import patch
from uuid import uuid4

import pytest
from django.db import ProgrammingError

from django_partitioned_audit.partitions.partition_info import PartitionInfo
from django_partitioned_audit.partitions.partition_manager_time_range import PartitionManager
from django_partitioned_audit.partitions.time_range_partitioning import MonthlyTimeRangeGenerator as MTRG
from tests.dummies import DummyAuditTableManager

# pylint: skip-file


@pytest.mark.django_db(transaction=True)
def test_create_partition(partitioned_table: str):
    pm = PartitionManager(audit_manager=DummyAuditTableManager(partitioned_table), time_range_generator=MTRG())
    assert not list(pm.get_existing_partitions())

    pm.create_partitions(
        [
            PartitionInfo.create(
                partitioned_table=partitioned_table,
                from_date=date(1999, 1, 1),
                to_date=date(1999, 2, 1),
            )
        ]
    )

    assert set(pm.get_existing_partitions()) == {PartitionInfo.parse(f"{partitioned_table}_19990101_19990201")}


@pytest.mark.django_db(transaction=True)
def test_create_second_long_partition_fails(partitioned_table_create: Callable):
    # Creates a `partitioned table` with a name that is not truncated by postgres, but is long enough
    # for partitions to be truncated when adding the suffix.
    # "abcdefghi_abcdefghi_abcdefghi_abcdefghi_abcdefghi_abcdefghi_abc"  bad
    # "abcdefghi_abcdefghi_abcdefghi_abcdefghi_abcdefghi_abcdefgh_1999"  bad
    # "abcdefghi_abcdefghi_abcdefghi_abcdefghi_abcdefghi_abcd_19990101"  bad
    # "abcdefghi_abcdefghi_abcdefghi_abcdefghi_abcdefghi_19990101_1999"  bad
    # "abcdefghi_abcdefghi_abcdefghi_abcdefghi_abcde_19990101_19990101"  good

    bad = f"abcdefghi_{uuid4().hex[0:9]}_{uuid4().hex[0:9]}_{uuid4().hex[0:9]}_{uuid4().hex[0:9]}_abcdefgh"
    partition_1 = PartitionInfo.create(bad, date(1999, 1, 1), date(1999, 2, 1))
    partition_2 = PartitionInfo.create(bad, date(1999, 2, 1), date(1999, 3, 1))

    partitioned_table_create(bad)

    with patch.object(PartitionManager, "_validate_partitioned_table", new_callable=Mock):
        pm = PartitionManager(audit_manager=DummyAuditTableManager(bad), time_range_generator=MTRG())
        pm.create_partitions([partition_1])
        with pytest.raises(ProgrammingError, match=r'relation.*abcdefghi_[a-f0-9_]+_abcdefgh_1999" already exists'):
            pm.create_partitions([partition_2])
