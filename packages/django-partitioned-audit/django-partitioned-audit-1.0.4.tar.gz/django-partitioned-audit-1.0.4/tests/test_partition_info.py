from datetime import date

import pytest

from django_partitioned_audit.partitions.partition_info import PartitionInfo


def test_partition_info_parse():
    partition_info = PartitionInfo.parse("some_partitioned_table_19980102_19990304")
    assert partition_info
    assert partition_info.partition == "some_partitioned_table_19980102_19990304"
    assert partition_info.partitioned_table == "some_partitioned_table"
    assert partition_info.from_date == date(1998, 1, 2)
    assert partition_info.to_date == date(1999, 3, 4)


@pytest.mark.parametrize(
    "table_name",
    [
        "some_partitioned_table_19980102_19970304",  # year after
        "some_partitioned_table_19980402_19980304",  # month after
        "some_partitioned_table_19990305_19990304",  # day after
        "some_partitioned_table_19990304_19990304",  # same day
    ],
)
def test_partition_info_parse_fails(table_name):
    with pytest.raises(ValueError):
        PartitionInfo.parse(table_name)


def test_partition_info_create():
    partition_info = PartitionInfo.create("foo", date(1998, 1, 2), date(1999, 3, 4))
    assert partition_info.partition == "foo_19980102_19990304"
    assert partition_info.from_date == date(1998, 1, 2)
    assert partition_info.to_date == date(1999, 3, 4)


def test_generate_create_partition():
    partition_info = PartitionInfo.create("foo", date(1998, 1, 2), date(1999, 3, 4))
    sql, params = partition_info.generate_create_partition()
    sql_line = " ".join([_.strip() for _ in sql.splitlines() if _.strip()])
    sql_line = " ".join([_.strip() for _ in sql_line.split() if _.strip()])
    sql_line = sql_line.lower()
    sql_line = sql_line.replace("%s", "{}")
    # not exactly the same interpolation done by db driver, but usable for tests
    final_sql = sql_line.format(*params)
    expected_sql = (
        """create table foo_19980102_19990304 """
        """partition of foo """
        """for values from (1998-01-02) to (1999-03-04);"""
    )
    assert final_sql == expected_sql
