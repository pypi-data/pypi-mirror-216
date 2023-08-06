import os
from datetime import date
from io import StringIO
from typing import List
from unittest.mock import PropertyMock
from unittest.mock import patch

import pytest
from django.core import management

from django_partitioned_audit.partitions.partition_manager_time_range import PartitionManager

# pylint: skip-file


def print_unindented(text: str):
    print("\n".join([line.strip() for line in text.splitlines()]))


def run_command(*command_args):
    with patch.object(PartitionManager, "today", new_callable=PropertyMock) as mock_today:
        mock_today.return_value = date(2022, 2, 22)
        out = StringIO()
        management.call_command(
            "manage_partition_tables",
            *command_args,
            verbosity=0,
            stdout=out,
        )
        lines: List[str] = out.getvalue().splitlines()
        print("")
        print(f"    $ manage.py manage_partition_tables {' '.join(command_args)}")
        for line in lines:
            print(f"    {line}")
        print("")


@pytest.mark.skipif(os.environ.get("TEST_README") != "1", reason="TEST_README")
@pytest.mark.django_db(transaction=True)
def test_simple_create(truncate_partitions):
    run_command("create", "--extra-days=60")


@pytest.mark.skipif(os.environ.get("TEST_README") != "1", reason="TEST_README")
@pytest.mark.django_db(transaction=True)
def test_sample_workflow(truncate_partitions):
    print_unindented(
        """
    Sample usage
    ++++++++++++

    If you want to have enough partition to handle next 90 days (around 3 months), you can use `--extra-days=90`.
    Because it's the first time we run the command, no partition exists, and the plan will report that all
    partitions need to be created::
    """
    )
    run_command("simulate", "--extra-days=90")
    print_unindented(
        """
    We can also see the plan if no extra days are requested (this way, we'll only create partitions for
    the current month::
    """
    )
    run_command("simulate", "--extra-days=0")
    print_unindented(
        """
    Now let's create the partitions::
    """
    )
    run_command("create", "--extra-days=0")
    print_unindented(
        """
    If we run the command and we pass `--extra-days=90`, the partition for the current month already exists, and
    only partitions for next months (to cover 90 days) will be created::
    """
    )
    run_command("create", "--extra-days=90")
    print_unindented(
        """
    We can use `list` to list existing partitions::
    """
    )
    run_command("list")


@pytest.mark.skipif(os.environ.get("TEST_README") != "1", reason="TEST_README")
@pytest.mark.django_db(transaction=True)
def test_sample_workflow_weekly(truncate_partitions):
    print_unindented(
        """
    Partition per week
    ++++++++++++++++++

    We can use one partition per week::
    """
    )
    run_command("create", "--extra-days=30", "--time-range-generator=WeeklyTimeRangeGenerator")


@pytest.mark.skipif(os.environ.get("TEST_README") != "1", reason="TEST_README")
@pytest.mark.django_db(transaction=True)
def test_sample_workflow_daily(truncate_partitions):
    print_unindented(
        """
    Partition per day
    +++++++++++++++++

    We can use one partition per day::
    """
    )
    run_command("create", "--extra-days=10", "--time-range-generator=DailyTimeRangeGenerator")
