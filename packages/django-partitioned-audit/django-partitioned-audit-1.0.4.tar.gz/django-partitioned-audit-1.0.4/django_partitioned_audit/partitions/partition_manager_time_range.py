from datetime import timedelta

from django_partitioned_audit.partitions.partition_info import PartitionInfo
from django_partitioned_audit.partitions.partition_info import TimeRange
from django_partitioned_audit.partitions.partition_manager_base import BasePartitionManager
from django_partitioned_audit.partitions.partition_manager_plan import Plan


class PartitionManager(BasePartitionManager):
    def generate_partition_info_for_current_period(self) -> PartitionInfo:
        """When there are partitions, we need to start with the one for current period"""
        from_to = self._time_range_generator.generate_partition_info_for_current_period(self.today)
        return PartitionInfo.create(self._partitioned_table, from_to.from_date, from_to.to_date)

    def new_partition(self, previous: PartitionInfo) -> PartitionInfo:
        from_to = self._time_range_generator.new_partition(TimeRange(previous.from_date, previous.to_date))
        return PartitionInfo.create(previous.partitioned_table, from_to.from_date, from_to.to_date)

    def generate_plan(self) -> Plan:
        """
        Generate `PartitionInfo` required to have partitions for at least `extra_days` days.
        """
        last_day_to_cover = self.today + timedelta(days=self._extra_days)
        plan: Plan = Plan()

        plan.existing_partitions.extend(self.get_existing_partitions())
        if not plan.last_partition:
            # no partition exists, we need at least one for the algorithm to work
            plan.partitions_to_create.append(self.generate_partition_info_for_current_period())

        while not plan.covers_date(last_day_to_cover):
            plan.partitions_to_create.append(self.new_partition(previous=plan.last_partition))

        plan.calculate_status(today=self.today, extra_days=self._extra_days)

        return plan
