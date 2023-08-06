import dataclasses
import sys
from typing import List

from django.core.management.base import BaseCommand

from django_partitioned_audit.partitions.partition_info import PartitionInfo
from django_partitioned_audit.partitions.partition_manager_plan import Plan
from django_partitioned_audit.partitions.partition_manager_plan import Status
from django_partitioned_audit.partitions.partition_manager_time_range import PartitionManager
from django_partitioned_audit.partitions.time_range_partitioning import DailyTimeRangeGenerator
from django_partitioned_audit.partitions.time_range_partitioning import MonthlyTimeRangeGenerator
from django_partitioned_audit.partitions.time_range_partitioning import WeeklyTimeRangeGenerator

ACTION_NAMES = ["list", "list-all", "simulate", "create"]

TIME_RANGE_GENERATORS = {
    "MonthlyTimeRangeGenerator": MonthlyTimeRangeGenerator,
    "WeeklyTimeRangeGenerator": WeeklyTimeRangeGenerator,
    "DailyTimeRangeGenerator": DailyTimeRangeGenerator,
}


@dataclasses.dataclass
class PrettyTableDummy:
    rows: List[List[str]] = dataclasses.field(default_factory=list)

    def add_row(self, row: List[str]):
        self.rows.append(row)

    def __str__(self):
        lines = [" | ".join([str(_) for _ in cols]) for cols in self.rows]
        return "\n".join(sorted(lines))


try:
    from prettytable import PrettyTable
except ImportError:
    PrettyTable = PrettyTableDummy


class Command(BaseCommand):
    help = "Makes sure all the required partition tables exists"

    def add_arguments(self, parser):
        parser.add_argument("actions", nargs="+", choices=ACTION_NAMES)
        parser.add_argument("--extra-days", type=int, default=PartitionManager.default_extra_days)
        parser.add_argument(
            "--time-range-generator",
            type=str,
            default="MonthlyTimeRangeGenerator",
            choices=list(TIME_RANGE_GENERATORS.keys()),
        )

    def handle(self, *args, **options):
        time_range_generator_class = TIME_RANGE_GENERATORS[options["time_range_generator"]]
        pm = PartitionManager(
            extra_days=options["extra_days"],
            time_range_generator=time_range_generator_class(),
        )

        for action in options["actions"]:
            if action == "list":
                self._run_list(pm, **options)
            elif action == "list-all":
                self._run_list(pm, list_all=True, **options)
            elif action == "simulate":
                self._run_simulate(pm, **options)
            elif action == "create":
                self._run_create(pm, **options)
            else:
                raise NotImplementedError(f"Action '{action}' not implemented")

    def _run_list(self, pm: PartitionManager, list_all=False, **options):
        pretty = PrettyTable()
        pretty.field_names = ["table_name", "from_date", "to_date"]
        pretty.padding_width = 2
        pretty.sortby = "table_name"
        pretty.align = "l"

        for table_name in pm.get_tables():
            pi = PartitionInfo.parse(table_name)
            if pi:
                pretty.add_row([pi.partition, pi.from_date, pi.to_date])
            else:
                if list_all:
                    pretty.add_row([table_name, "", ""])

        self.stdout.write(str(pretty))

    def _run_simulate(self, pm: PartitionManager, exit_with_status=False, **options) -> Plan:
        pretty = PrettyTable()
        pretty.field_names = ["table_name", "from_date", "to_date", "status"]
        pretty.padding_width = 2
        pretty.sortby = "table_name"
        pretty.align = "l"
        simulation = pm.generate_plan()

        status_prefix = "⚠" if simulation.status == Status.MISSING_CURRENT else "❌"
        for pi in simulation.existing_partitions:
            pretty.add_row([pi.partition, pi.from_date, pi.to_date, "✓ exists"])
        for pi in simulation.partitions_to_create:
            pretty.add_row([pi.partition, pi.from_date, pi.to_date, f"{status_prefix} to create"])

        self.stdout.write(str(pretty))

        if exit_with_status:
            if simulation.status == Status.OK:
                sys.exit(0)
            elif simulation.status == Status.MISSING_CURRENT:
                print("ERROR: required partition to store data for current period do not exist", file=self.stdout)
                sys.exit(1)
            elif simulation.status == Status.MISSING_NEXT:
                sys.exit(0)
            else:
                raise NotImplementedError(f"Unexpected status: {simulation.status}")

        return simulation

    def _run_create(self, pm: PartitionManager, **options):
        plan = self._run_simulate(pm, exit_with_status=False)

        for pi in plan.partitions_to_create:
            sql, params = pi.generate_create_partition()
            sql_line = " ".join([_.strip() for _ in sql.splitlines() if _.strip()])
            self.stdout.write(f"sql: {sql_line} / params: {params}\n")

        if plan.partitions_to_create:
            pm.create_partitions(plan.partitions_to_create)
        else:
            self.stdout.write("All required partitions exists :D\n")
