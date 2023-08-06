import os
import pathlib
import re
from datetime import date
from typing import List
from typing import Tuple
from typing import Type

from django.db import ProgrammingError
from django.db import transaction
from django.db.models import Model

from django_partitioned_audit.audit_table.audit_table_manager import AuditTableManager
from django_partitioned_audit.models import AdvancedAuditEntry


class AdvancedAuditTableManager(AuditTableManager):
    """
    Audit table implementation based on:
    - https://wiki.postgresql.org/wiki/Audit_trigger_91plus
    - https://github.com/2ndQuadrant/audit-trigger
    """

    @property
    def partitioned_table_name(self) -> str:
        return "logged_actions"

    @property
    def model(self) -> Type[Model]:
        return AdvancedAuditEntry

    def generate_create_partition(
        self, partition_name: str, partitioned_table: str, from_date: date, to_date: date
    ) -> Tuple[str, List[object]]:
        # TODO: find a way to escape tables names, so we don't have to use that regex
        sql_statement = f"""
        CREATE TABLE {partition_name}
            PARTITION OF {partitioned_table}
            FOR VALUES FROM (%s) TO (%s);
        """
        params = [from_date, to_date]
        return sql_statement, params

    def create_partitioned_table(self, cursor):
        sql = pathlib.Path(__file__).parent.resolve() / "advanced_audit_table_manager.sql"
        assert sql.exists()
        try:
            with transaction.atomic():
                cursor.execute(f"SELECT * FROM {self.partitioned_table_name} limit 1")
            audit_table_exists = True
        except ProgrammingError as err:
            audit_table_exists = None
            if err.args[0]:
                if isinstance(err.args[0], str):
                    message = err.args[0].splitlines()[0]
                    if re.search(rf"relation.*{self.partitioned_table_name}.*does not exist", message):
                        audit_table_exists = False
            if audit_table_exists is None:
                raise

        if not audit_table_exists:
            cursor.execute(sql.read_text())
            cursor.execute(
                """
            CREATE OR REPLACE VIEW logged_actions_view AS (
                SELECT
                    logged_actions.*,
                    hstore_to_jsonb(logged_actions.row_data) as "row_data_json",
                    hstore_to_jsonb(logged_actions.changed_fields) as "changed_fields_json",
                    ROW_NUMBER() OVER () as "synthetic_id"
                FROM
                    logged_actions
            );
            """
            )
            # TODO: remove `synthetic_id` (only reason to have it is to make the view read-only)

    def enable_audit_for_table(self, cursor, table_name: str):
        sql = "SELECT audit_table(%s);"
        cursor.execute(sql, [table_name])

    def disable_audit_for_table(self, cursor, table_name: str):
        cursor.execute(
            "DROP TRIGGER IF EXISTS audit_trigger_row ON {table_name};".format(
                table_name=table_name,  # FIXME: properly escape this to guarantee avoid SQL injection
            )
        )
        cursor.execute(
            "DROP TRIGGER IF EXISTS audit_trigger_stm ON {table_name};".format(
                table_name=table_name,  # FIXME: properly escape this to guarantee avoid SQL injection
            )
        )

    def drop_all(self, cursor):
        assert "PYTEST_CURRENT_TEST" in os.environ
        for table_name, trigger_name in self.get_triggers(cursor):
            if trigger_name in ["audit_trigger_row", "audit_trigger_stm"]:
                cursor.execute(f"DROP TRIGGER IF EXISTS {trigger_name} ON {table_name}")

        drop_partitions = """
        DO
        $src$
        DECLARE
            item VARCHAR;
        BEGIN
            FOR item IN
                SELECT table_name FROM information_schema.tables WHERE table_name LIKE %s
            LOOP
                PERFORM 'DROP TABLE IF EXISTS ' || item;
            END LOOP;
        END;
        $src$
        """
        params = [f"{self.partitioned_table_name}_????????_????????"]
        cursor.execute(drop_partitions, params)

        cursor.execute(f"DROP VIEW IF EXISTS {self.partitioned_table_name}_view")
        cursor.execute(f"DROP TABLE IF EXISTS {self.partitioned_table_name}")
        return
