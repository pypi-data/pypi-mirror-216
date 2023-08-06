import random
from datetime import date

import pytest

from django_partitioned_audit.partitions.partition_info import PartitionInfo
from django_partitioned_audit.partitions.partition_manager_plan import Plan


def test_valid_empty_plan():
    plan = Plan()
    assert plan.sorted_all == []
    assert plan.sorted_existing == []
    assert plan.sorted_to_create == []
    assert plan.last_partition is None
    assert plan.covers_date(date(1000, 1, 1)) is False
    assert plan.covers_date(date(2999, 1, 1)) is False
    plan.validate_existing_partitions()
    plan.validate_to_create()
    plan.validate_all()


def test_valid_plan_with_existing():
    plan = Plan()
    partition = PartitionInfo.create("part", date(1991, 1, 1), date(1991, 2, 1))
    plan.existing_partitions.append(partition)
    assert plan.sorted_all == [partition]
    assert plan.sorted_existing == [partition]
    assert plan.sorted_to_create == []
    assert plan.last_partition == partition
    assert plan.covers_date(date(1990, 12, 31)) is False
    assert plan.covers_date(date(1991, 1, 1))
    assert plan.covers_date(date(1991, 1, 31))
    assert plan.covers_date(date(1991, 2, 1)) is False
    assert plan.covers_date(date(1000, 1, 1)) is False
    assert plan.covers_date(date(2999, 1, 1)) is False
    plan.validate_existing_partitions()
    plan.validate_to_create()
    plan.validate_all()


def test_valid_plan_with_partitions_to_create():
    plan = Plan()
    partition = PartitionInfo.create("part", date(1991, 1, 1), date(1991, 2, 1))
    plan.partitions_to_create.append(partition)
    assert plan.sorted_all == [partition]
    assert plan.sorted_existing == []
    assert plan.sorted_to_create == [partition]
    assert plan.last_partition == partition
    assert plan.covers_date(date(1990, 12, 31)) is False
    assert plan.covers_date(date(1991, 1, 1))
    assert plan.covers_date(date(1991, 1, 31))
    assert plan.covers_date(date(1991, 2, 1)) is False
    assert plan.covers_date(date(1000, 1, 1)) is False
    assert plan.covers_date(date(2999, 1, 1)) is False
    plan.validate_existing_partitions()
    plan.validate_to_create()
    plan.validate_all()


def test_valid_plan_with_both():
    plan = Plan()
    partition_existing = PartitionInfo.create("part", date(1991, 1, 1), date(1991, 2, 1))
    partition_create = PartitionInfo.create("part", date(1991, 2, 1), date(1991, 3, 1))
    plan.existing_partitions.append(partition_existing)
    plan.partitions_to_create.append(partition_create)
    assert plan.sorted_all == [partition_existing, partition_create]
    assert plan.sorted_existing == [partition_existing]
    assert plan.sorted_to_create == [partition_create]
    assert plan.last_partition == partition_create
    assert plan.covers_date(date(1990, 12, 31)) is False
    assert plan.covers_date(date(1991, 1, 1))
    assert plan.covers_date(date(1991, 1, 31))
    assert plan.covers_date(date(1991, 2, 1))
    assert plan.covers_date(date(1991, 2, 28))
    assert plan.covers_date(date(1991, 3, 1)) is False
    assert plan.covers_date(date(1000, 1, 1)) is False
    assert plan.covers_date(date(2999, 1, 1)) is False
    plan.validate_existing_partitions()
    plan.validate_to_create()
    plan.validate_all()


def test_valid_plan_with_many():
    plan = Plan()
    partitions_existing = [
        PartitionInfo.create("part", date(1991, 1, 1), date(1991, 2, 1)),
        PartitionInfo.create("part", date(1991, 2, 1), date(1991, 3, 1)),
        PartitionInfo.create("part", date(1991, 3, 1), date(1991, 4, 1)),
        PartitionInfo.create("part", date(1991, 4, 1), date(1991, 5, 1)),
    ]
    partitions_create = [
        PartitionInfo.create("part", date(1991, 5, 1), date(1991, 6, 1)),
        PartitionInfo.create("part", date(1991, 6, 1), date(1991, 7, 1)),
        PartitionInfo.create("part", date(1991, 7, 1), date(1991, 8, 1)),
    ]
    plan.existing_partitions.extend(partitions_existing)
    plan.partitions_to_create.extend(partitions_create)
    random.shuffle(plan.existing_partitions)
    random.shuffle(plan.partitions_to_create)
    assert plan.sorted_all == partitions_existing + partitions_create
    assert plan.sorted_existing == partitions_existing
    assert plan.sorted_to_create == partitions_create
    assert plan.last_partition == partitions_create[-1]
    assert plan.covers_date(date(1990, 12, 31)) is False
    assert plan.covers_date(date(1991, 1, 1))
    assert plan.covers_date(date(1991, 1, 31))
    assert plan.covers_date(date(1991, 2, 1))
    assert plan.covers_date(date(1991, 2, 28))
    assert plan.covers_date(date(1991, 7, 31))
    assert plan.covers_date(date(1991, 8, 1)) is False
    assert plan.covers_date(date(1000, 1, 1)) is False
    assert plan.covers_date(date(2999, 1, 1)) is False
    plan.validate_existing_partitions()
    plan.validate_to_create()
    plan.validate_all()


def test_invalid_existing_partitions():
    plan = Plan(
        existing_partitions=[
            PartitionInfo.create("part", date(1991, 1, 1), date(1991, 2, 1)),
            # PartitionInfo.create("part", date(1991, 2, 1), date(1991, 3, 1)),
            PartitionInfo.create("part", date(1991, 3, 1), date(1991, 4, 1)),
        ],
        partitions_to_create=[
            PartitionInfo.create("part", date(1991, 4, 1), date(1991, 5, 1)),
            PartitionInfo.create("part", date(1991, 5, 1), date(1991, 6, 1)),
            PartitionInfo.create("part", date(1991, 6, 1), date(1991, 7, 1)),
            PartitionInfo.create("part", date(1991, 7, 1), date(1991, 8, 1)),
        ],
    )
    with pytest.raises(Exception):
        plan.validate_existing_partitions()
    plan.validate_to_create()
    with pytest.raises(Exception):
        plan.validate_all()


def test_invalid_partitions_to_create():
    plan = Plan(
        existing_partitions=[
            PartitionInfo.create("part", date(1991, 1, 1), date(1991, 2, 1)),
            PartitionInfo.create("part", date(1991, 2, 1), date(1991, 3, 1)),
            PartitionInfo.create("part", date(1991, 3, 1), date(1991, 4, 1)),
        ],
        partitions_to_create=[
            PartitionInfo.create("part", date(1991, 4, 1), date(1991, 5, 1)),
            # PartitionInfo.create("part", date(1991, 5, 1), date(1991, 6, 1)),
            PartitionInfo.create("part", date(1991, 6, 1), date(1991, 7, 1)),
            PartitionInfo.create("part", date(1991, 7, 1), date(1991, 8, 1)),
        ],
    )
    plan.validate_existing_partitions()
    with pytest.raises(Exception):
        plan.validate_to_create()
    with pytest.raises(Exception):
        plan.validate_all()


def test_invalid_partitions_to_create_missing_day():
    plan = Plan(
        existing_partitions=[
            PartitionInfo.create("part", date(1991, 1, 1), date(1991, 2, 1)),
            PartitionInfo.create("part", date(1991, 2, 2), date(1991, 3, 1)),  # missing day here
            PartitionInfo.create("part", date(1991, 3, 1), date(1991, 4, 1)),
        ],
        partitions_to_create=[
            PartitionInfo.create("part", date(1991, 4, 1), date(1991, 5, 1)),
            PartitionInfo.create("part", date(1991, 5, 1), date(1991, 6, 2)),  # missing day here
            PartitionInfo.create("part", date(1991, 6, 1), date(1991, 7, 1)),
            PartitionInfo.create("part", date(1991, 7, 1), date(1991, 8, 1)),
        ],
    )
    with pytest.raises(Exception):
        plan.validate_existing_partitions()
    with pytest.raises(Exception):
        plan.validate_to_create()
    with pytest.raises(Exception):
        plan.validate_all()
