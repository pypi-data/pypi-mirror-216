from unittest.mock import Mock
from unittest.mock import patch
from uuid import uuid4

import pytest

from django_partitioned_audit.partitions.partition_manager_time_range import PartitionManager
from django_partitioned_audit.partitions.time_range_partitioning import MonthlyTimeRangeGenerator as MTRG
from tests.dummies import DummyAuditTableManager


@pytest.mark.django_db(transaction=True)
def test_short_name_works(partitioned_table: str):
    pm = PartitionManager(time_range_generator=MTRG())
    assert partitioned_table in pm.get_tables()


@pytest.mark.django_db(transaction=True)
def test_long_name_is_truncated(very_long_named_partitioned_table: str):
    with patch.object(PartitionManager, "_validate_partitioned_table", new_callable=Mock) as mock:
        mock.return_value = None
        pm = PartitionManager(
            audit_manager=DummyAuditTableManager(very_long_named_partitioned_table), time_range_generator=MTRG()
        )
        assert very_long_named_partitioned_table not in pm.get_tables()
        assert very_long_named_partitioned_table[0:63] in pm.get_tables()


@pytest.mark.django_db(transaction=True)
def test_partition_manager_fails_with_long_names():
    # "abcdefghi_abcdefghi_abcdefghi_abcdefghi_abcdefghi_abcdefghi_abc"
    # "abcdefghi_abcdefghi_abcdefghi_abcdefghi_abcde_19990101_19990101"
    valid_partitioned_table = f"abcdefghi_{uuid4().hex[0:9]}_{uuid4().hex[0:9]}_{uuid4().hex[0:9]}_abcde"
    invalid_partitioned_table = f"abcdefghi_{uuid4().hex[0:9]}_{uuid4().hex[0:9]}_{uuid4().hex[0:9]}_abcdef"
    partition_suffix = "_19990101_19990201"

    assert len(valid_partitioned_table) == 45
    assert len(invalid_partitioned_table) == 46
    assert len(partition_suffix) == 18

    assert PartitionManager(audit_manager=DummyAuditTableManager(valid_partitioned_table), time_range_generator=MTRG())
    with pytest.raises(ValueError):
        assert PartitionManager(
            audit_manager=DummyAuditTableManager(invalid_partitioned_table), time_range_generator=MTRG()
        )
