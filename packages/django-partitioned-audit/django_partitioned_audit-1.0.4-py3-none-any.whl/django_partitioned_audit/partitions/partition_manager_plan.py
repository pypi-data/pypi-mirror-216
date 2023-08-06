import dataclasses
from dataclasses import field
from datetime import date
from datetime import timedelta
from enum import Enum
from typing import Iterator
from typing import List
from typing import Optional

from django_partitioned_audit.partitions.partition_info import PartitionInfo


class Status(Enum):
    OK = 1
    MISSING_NEXT = 2
    MISSING_CURRENT = 3


@dataclasses.dataclass
class Plan:
    existing_partitions: List[PartitionInfo] = field(default_factory=list)
    partitions_to_create: List[PartitionInfo] = field(default_factory=list)
    status: Optional[Status] = None

    @property
    def sorted_existing(self) -> List[PartitionInfo]:
        return sorted(self.existing_partitions, key=lambda _: _.from_date)

    @property
    def sorted_to_create(self) -> List[PartitionInfo]:
        return sorted(self.partitions_to_create, key=lambda _: _.from_date)

    @property
    def sorted_all(self) -> List[PartitionInfo]:
        return sorted(self.partitions_to_create + self.existing_partitions, key=lambda _: _.from_date)

    @property
    def last_partition(self) -> Optional[PartitionInfo]:
        try:
            return self.sorted_all[-1]
        except IndexError:
            return None

    def covers_date(self, day_to_cover: date) -> bool:
        return self.get_partition_for_date(self.sorted_all, day_to_cover) is not None

    @classmethod
    def get_partition_for_date(cls, partitions: List[PartitionInfo], reference_day: date) -> Optional[PartitionInfo]:
        for part_info in partitions:
            if part_info.from_date <= reference_day < part_info.to_date:
                return part_info
        return None

    @classmethod
    def _validate(cls, partitions: Iterator[PartitionInfo]):
        # TODO: when empty, should we fail?
        last_to_date = None
        for pi in partitions:
            if last_to_date is None:
                last_to_date = pi.to_date
            else:
                if last_to_date != pi.from_date:
                    raise Exception(f"Invalid: last_to_date={last_to_date} pi={pi}")
                last_to_date = pi.to_date

    def validate_existing_partitions(self):
        self._validate(self.sorted_existing)

    def validate_to_create(self):
        self._validate(self.sorted_to_create)

    def validate_all(self):
        self._validate(self.sorted_all)

    def calculate_status(self, today: date, extra_days: int):
        assert self.status is None
        assert extra_days >= 0
        assert self.existing_partitions or self.partitions_to_create  # one or both must contain something
        if self.existing_partitions and not self.partitions_to_create:
            # no new partitions, this means all is good, current time range and extra days are covered
            self.status = Status.OK
            # Just in case, check today is covered by existing
            assert self.get_partition_for_date(self.sorted_existing, today) is not None
            # Juts in case, check extra days
            assert self.sorted_all[-1].to_date >= today + timedelta(days=extra_days)
            return

        if not self.existing_partitions and self.partitions_to_create:
            # no existing partitions, this must be the first time the command is run
            self.status = Status.MISSING_CURRENT
            # Just in case, check today is covered by 'to create'
            assert self.get_partition_for_date(self.sorted_to_create, today) is not None
            # Juts in case, check extra days
            assert self.sorted_all[-1].to_date >= today + timedelta(days=extra_days)
            return

        if self.existing_partitions and self.partitions_to_create:
            # both existing partitions and to create... let's see is we need to create for current time range
            current_time_range_in_existing = self.get_partition_for_date(self.sorted_existing, today) is not None
            current_time_range_in_to_create = self.get_partition_for_date(self.sorted_to_create, today) is not None
            assert {current_time_range_in_existing, current_time_range_in_to_create} == {True, False}

            if current_time_range_in_to_create:
                # This is the worst situation. There are existing tables, this is not the first time the system
                # is run, but there was no partition for current time. If the partitioned table was in use, the
                # system might have lacked the required partitions to be able to insert data.
                self.status = Status.MISSING_CURRENT
                # Just in case, check today is covered by 'to create'
                assert self.get_partition_for_date(self.sorted_to_create, today) is not None
            else:
                self.status = Status.MISSING_NEXT
                # Just in case, check today is covered by existing
                assert self.get_partition_for_date(self.sorted_existing, today) is not None

            # Juts in case, check extra days
            assert self.sorted_all[-1].to_date >= today + timedelta(days=extra_days)
