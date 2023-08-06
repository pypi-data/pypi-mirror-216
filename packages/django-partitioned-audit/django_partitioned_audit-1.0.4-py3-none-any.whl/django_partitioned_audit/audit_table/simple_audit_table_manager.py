import os
from datetime import date
from typing import List
from typing import Tuple
from typing import Type

from django.db.models import Model

from django_partitioned_audit.audit_table.audit_table_manager import AuditTableManager
from django_partitioned_audit.models import SimpleAuditEntry


class SimpleAuditTableManager(AuditTableManager):
    @property
    def partitioned_table_name(self) -> str:
        return "audit_simple"

    @property
    def model(self) -> Type[Model]:
        return SimpleAuditEntry

    def create_partitioned_table(self, cursor):
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS audit_simple (
            object_table character varying(63) NOT NULL,
            object_payload JSONB NOT NULL,
            audit_entry_created timestamp with time zone DEFAULT now() NOT NULL,
            audit_entry_created_statement_timestamp timestamp with time zone DEFAULT statement_timestamp() NOT NULL,
            audit_txid_current bigint NOT NULL,
            audit_operation character varying(1) NOT NULL
        ) PARTITION BY RANGE (audit_entry_created);
        """
        )
        cursor.execute(
            """
        CREATE INDEX IF NOT EXISTS idx_audit_simple
            ON audit_simple
            USING GIN (object_payload);
        """
        )
        cursor.execute(
            """
        CREATE OR REPLACE VIEW audit_simple_view AS (
            SELECT
                ROW_NUMBER() OVER () as "id",
                object_table,
                object_payload,
                audit_entry_created,
                audit_entry_created_statement_timestamp,
                audit_txid_current,
                audit_operation
            FROM
                audit_simple
        );
        """
        )
        cursor.execute(
            """
        CREATE OR REPLACE FUNCTION trigger_audit_entry_creator_func_v2() RETURNS TRIGGER AS $scr$
            DECLARE
                object_payload jsonb;
                trigger_operation varchar;
            BEGIN
                IF (TG_OP = 'INSERT') THEN
                    object_payload  = to_jsonb(NEW);
                    trigger_operation = 'I';
                ELSIF (TG_OP = 'UPDATE') THEN
                    object_payload  = to_jsonb(NEW);
                    trigger_operation = 'U';
                ELSIF (TG_OP = 'DELETE') THEN
                    object_payload  = to_jsonb(OLD);
                    trigger_operation = 'D';
                ELSE
                    RAISE EXCEPTION 'Unexpected TG_OP = %', TG_OP;
                END IF;

                INSERT INTO audit_simple (
                        object_table,
                        object_payload,
                        audit_txid_current,
                        audit_operation
                    )
                    SELECT
                        TG_TABLE_NAME,
                        object_payload,
                        txid_current(),
                        trigger_operation;
                RETURN NULL;
            END;
        $scr$ LANGUAGE plpgsql;
        """
        )

    def enable_audit_for_table(self, cursor, table_name: str):
        sql = """
        -- https://www.postgresql.org/message-id/1360944248465-5745434.post%40n5.nabble.com
        DO
        $src$
        BEGIN
        IF NOT EXISTS(SELECT * FROM information_schema.triggers
                      WHERE event_object_table = '{table_name}' AND trigger_name = '{trigger_name}')
            THEN

                CREATE TRIGGER {trigger_name} AFTER INSERT OR UPDATE OR DELETE ON {table_name}
                    FOR EACH ROW EXECUTE FUNCTION trigger_audit_entry_creator_func_v2();

            END IF;
        END;
        $src$
        """.format(
            table_name=table_name,  # FIXME: properly escape this to guarantee avoid SQL injection
            trigger_name="trigger_audit_entry_creator_trigger",
        )
        cursor.execute(sql)

    def disable_audit_for_table(self, cursor, table_name: str):
        sql = "DROP TRIGGER IF EXISTS {trigger_name} ON {table_name};".format(
            table_name=table_name,  # FIXME: properly escape this to guarantee avoid SQL injection
            trigger_name="trigger_audit_entry_creator_trigger",
        )
        cursor.execute(sql)

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

    def drop_all(self, cursor):
        assert "PYTEST_CURRENT_TEST" in os.environ

        # we need 'IF EXISTS' because data on `information_schema` is not in-sync with transaction,
        # we can get from there references to triggers, etc. that no longer exists.
        # TODO: is this the real explanation?

        for table_name, trigger_name in self.get_triggers(cursor):
            if trigger_name == "trigger_audit_entry_creator_trigger":
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
                PERFORM 'DROP TABLE ' || item;
            END LOOP;
        END;
        $src$
        """
        params = [f"{self.partitioned_table_name}_????????_????????"]
        cursor.execute(drop_partitions, params)

        cursor.execute(f"DROP VIEW IF EXISTS {self.partitioned_table_name}_view")
        cursor.execute(f"DROP TABLE IF EXISTS {self.partitioned_table_name}")
