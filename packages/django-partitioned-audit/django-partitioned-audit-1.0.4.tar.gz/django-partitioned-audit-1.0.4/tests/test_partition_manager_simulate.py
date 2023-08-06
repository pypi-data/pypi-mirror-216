from datetime import date
from typing import Type
from unittest.mock import Mock
from unittest.mock import PropertyMock
from unittest.mock import patch

import pytest

from django_partitioned_audit.partitions.partition_info import PartitionInfo
from django_partitioned_audit.partitions.partition_manager_plan import Plan
from django_partitioned_audit.partitions.partition_manager_plan import Status
from django_partitioned_audit.partitions.partition_manager_time_range import PartitionManager
from django_partitioned_audit.partitions.time_range_partitioning import DailyTimeRangeGenerator
from django_partitioned_audit.partitions.time_range_partitioning import MonthlyTimeRangeGenerator
from django_partitioned_audit.partitions.time_range_partitioning import TimeRangeGenerator
from django_partitioned_audit.partitions.time_range_partitioning import WeeklyTimeRangeGenerator
from tests.conftest import skipifadvanced


class MonthlyScenario:
    prev2: PartitionInfo = PartitionInfo.parse("audit_simple_18770101_18770201")
    prev1: PartitionInfo = PartitionInfo.parse("audit_simple_18770201_18770301")
    cur: PartitionInfo = PartitionInfo.parse("audit_simple_18770301_18770401")
    next1: PartitionInfo = PartitionInfo.parse("audit_simple_18770401_18770501")
    next2: PartitionInfo = PartitionInfo.parse("audit_simple_18770501_18770601")
    extra_days: int = 45
    extra_days_current_time_range: int = 9  # `today=1877-03-22`, 9 days left in this month
    tmg_impl: Type[TimeRangeGenerator] = MonthlyTimeRangeGenerator


class WeeklyScenario:
    prev2: PartitionInfo = PartitionInfo.parse("audit_simple_18770308_18770315")
    prev1: PartitionInfo = PartitionInfo.parse("audit_simple_18770315_18770322")
    cur: PartitionInfo = PartitionInfo.parse("audit_simple_18770322_18770329")
    next1: PartitionInfo = PartitionInfo.parse("audit_simple_18770329_18770405")
    next2: PartitionInfo = PartitionInfo.parse("audit_simple_18770405_18770412")
    extra_days: int = 18
    extra_days_current_time_range: int = 6
    tmg_impl: Type[TimeRangeGenerator] = WeeklyTimeRangeGenerator


class DailyScenario:
    prev2: PartitionInfo = PartitionInfo.parse("audit_simple_18770320_18770321")
    prev1: PartitionInfo = PartitionInfo.parse("audit_simple_18770321_18770322")
    cur: PartitionInfo = PartitionInfo.parse("audit_simple_18770322_18770323")
    next1: PartitionInfo = PartitionInfo.parse("audit_simple_18770323_18770324")
    next2: PartitionInfo = PartitionInfo.parse("audit_simple_18770324_18770325")
    extra_days: int = 2
    extra_days_current_time_range: int = 0
    tmg_impl: Type[TimeRangeGenerator] = DailyTimeRangeGenerator


def generate_scenarios():
    for scenario in [MonthlyScenario, WeeklyScenario, DailyScenario]:
        # partitions for current period is missing
        yield (
            "part-cur-time-range-missing-1",
            [],
            0,
            Status.MISSING_CURRENT,
            [scenario.cur],
            scenario.tmg_impl,
            # let's force expansion
        )
        yield (
            "part-cur-time-range-missing-2",
            [scenario.prev2, scenario.prev1],
            0,
            Status.MISSING_CURRENT,
            [scenario.cur],
            scenario.tmg_impl,
        )
        yield (
            "part-cur-time-range-missing-3",
            [],
            scenario.extra_days,
            Status.MISSING_CURRENT,
            [scenario.cur, scenario.next1, scenario.next2],
            scenario.tmg_impl,
        )
        yield (
            "part-cur-time-range-missing-4",
            [scenario.prev2, scenario.prev1],
            scenario.extra_days,
            Status.MISSING_CURRENT,
            [scenario.cur, scenario.next1, scenario.next2],
            scenario.tmg_impl,
        )
        # partitions for next periods is missing
        yield (
            "cur-ok-but-extra-days-missing-1",
            [scenario.cur],
            scenario.extra_days,
            Status.MISSING_NEXT,
            [scenario.next1, scenario.next2],
            scenario.tmg_impl,
        )
        yield (
            "cur-ok-but-extra-days-missing-2",
            [scenario.prev2, scenario.prev1, scenario.cur],
            scenario.extra_days,
            Status.MISSING_NEXT,
            [scenario.next1, scenario.next2],
            scenario.tmg_impl,
        )
        # all good
        yield (
            "all-good-1",
            [scenario.cur],
            0,
            Status.OK,
            [],
            scenario.tmg_impl,
        )
        yield (
            "all-good-2",
            [scenario.cur],
            scenario.extra_days_current_time_range,
            Status.OK,
            [],
            scenario.tmg_impl,
        )
        yield (
            "all-good-3",
            [scenario.cur, scenario.next1, scenario.next2],
            scenario.extra_days,
            Status.OK,
            [],
            scenario.tmg_impl,
        )
        yield (
            "all-good-4",
            [scenario.prev2, scenario.prev1, scenario.cur, scenario.next1, scenario.next2],
            scenario.extra_days,
            Status.OK,
            [],
            scenario.tmg_impl,
        )


scenarios = list(generate_scenarios())


@skipifadvanced
@pytest.mark.parametrize("desc,existing_partitions,extra_days,exp_status,exp_new,trg_class", scenarios)
def test_simulate_scenarios(desc, existing_partitions, extra_days, exp_status, exp_new, trg_class):
    assert all([isinstance(_, PartitionInfo) for _ in existing_partitions])
    assert isinstance(extra_days, int)
    assert 0 <= extra_days <= 365
    assert exp_status in {Status.OK, Status.MISSING_CURRENT, Status.MISSING_NEXT}
    assert all([isinstance(_, PartitionInfo) for _ in exp_new])

    pm = PartitionManager(time_range_generator=trg_class(), extra_days=extra_days)
    with patch.object(PartitionManager, "get_existing_partitions", new_callable=Mock) as mock_partitions:
        with patch.object(PartitionManager, "today", new_callable=PropertyMock) as mock_today:
            mock_partitions.return_value = existing_partitions
            mock_today.return_value = date(1877, 3, 22)
            plan: Plan = pm.generate_plan()

            assert set(plan.existing_partitions) == set(existing_partitions)
            assert set(plan.partitions_to_create) == set(exp_new)
            assert plan.status is not None
            assert plan.status == exp_status
