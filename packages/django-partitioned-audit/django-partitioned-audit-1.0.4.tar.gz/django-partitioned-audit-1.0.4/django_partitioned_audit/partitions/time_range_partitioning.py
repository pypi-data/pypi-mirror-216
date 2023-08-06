import dataclasses
from datetime import date
from datetime import timedelta

from django_partitioned_audit.partitions.partition_info import PartitionInfo
from django_partitioned_audit.partitions.partition_info import TimeRange


class TimeRangeGenerator:
    def generate_partition_info_for_current_period(self, today: date) -> PartitionInfo:
        raise NotImplementedError()

    def new_partition(self, previous: TimeRange) -> TimeRange:
        raise NotImplementedError()


#
# Rolling month partitioning
#


@dataclasses.dataclass
class YearMonth:
    year: int
    month: int

    def incr_month(self) -> "YearMonth":
        assert 1 <= self.month <= 12
        if self.month == 12:
            self.year += 1
            self.month = 1
        else:
            self.month += 1
        return self

    def as_date(self, day_of_month=1) -> date:
        assert self.year > 0
        assert 1 <= self.month <= 12
        assert 1 <= day_of_month <= 31
        return date(self.year, self.month, day_of_month)

    @classmethod
    def new_from_date(cls, reference: date) -> "YearMonth":
        return YearMonth(year=reference.year, month=reference.month)


class MonthlyTimeRangeGenerator(TimeRangeGenerator):
    def generate_partition_info_for_current_period(self, today: date) -> TimeRange:
        range_start = YearMonth(today.year, today.month).as_date()
        range_end = YearMonth.new_from_date(today).incr_month().as_date()
        return TimeRange(range_start, range_end)

    def new_partition(self, previous: TimeRange) -> TimeRange:
        new_range_start = previous.to_date
        new_range_end = YearMonth.new_from_date(previous.to_date).incr_month().as_date()
        return TimeRange(new_range_start, new_range_end)


class WeeklyTimeRangeGenerator(TimeRangeGenerator):
    def generate_partition_info_for_current_period(self, today: date) -> TimeRange:
        range_start = today
        range_end = range_start + timedelta(days=7)
        return TimeRange(range_start, range_end)

    def new_partition(self, previous: TimeRange) -> TimeRange:
        new_range_start = previous.to_date
        new_range_end = new_range_start + timedelta(days=7)
        return TimeRange(new_range_start, new_range_end)


class DailyTimeRangeGenerator(TimeRangeGenerator):
    def generate_partition_info_for_current_period(self, today: date) -> TimeRange:
        range_start = today
        range_end = range_start + timedelta(days=1)
        return TimeRange(range_start, range_end)

    def new_partition(self, previous: TimeRange) -> TimeRange:
        new_range_start = previous.to_date
        new_range_end = new_range_start + timedelta(days=1)
        return TimeRange(new_range_start, new_range_end)


class NotImplementedTimeRangeGenerator(TimeRangeGenerator):
    def generate_partition_info_for_current_period(self, today: date) -> TimeRange:
        raise NotImplementedError()

    def new_partition(self, previous: TimeRange) -> TimeRange:
        raise NotImplementedError()
