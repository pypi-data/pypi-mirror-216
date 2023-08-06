import logging

from django.apps import AppConfig
from django.db import connections
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from django_partitioned_audit.audit_table.audit_table_manager import AuditTableManager
from django_partitioned_audit.utils import get_disabled_models
from django_partitioned_audit.utils import get_enabled_models

logger = logging.getLogger(__name__)


@receiver(post_migrate)
def audit_run_post_migrate(app_config: AppConfig, verbosity, using, **kwargs):  # pylint: disable=unused-argument
    enabled_models = set(get_enabled_models(app_config))
    disabled_models = set(get_disabled_models(app_config))

    if disabled_models & enabled_models:
        print(f"Model are at the same time 'enabled' and 'disabled': {disabled_models & enabled_models}")

    disabled_models = disabled_models - enabled_models

    with connections[using].cursor() as cursor:
        # For now, we use the 'using' connection we received. Not sure if that's the best approach.
        audit_table_manager: AuditTableManager = AuditTableManager.get_implementation()

        # Let's (re)create the partitioned table and other objects
        audit_table_manager.create_partitioned_table(cursor)

        # Let's create the triggers
        for model_class_name in enabled_models:
            model_class = app_config.get_model(model_class_name)
            table_name = model_class._meta.db_table  # pylint: disable=protected-access
            if verbosity >= 1:
                print(f" - Enable auditing for '{model_class}' (table '{table_name}')")
            audit_table_manager.enable_audit_for_table(cursor, table_name)

        # and remove the ones that needs to be removed
        for model_class_name in disabled_models:
            model_class = app_config.get_model(model_class_name)
            table_name = model_class._meta.db_table  # pylint: disable=protected-access
            if verbosity >= 1:
                print(f" - Disabling auditing for '{model_class}' (table '{table_name}')")
            audit_table_manager.disable_audit_for_table(cursor, table_name)


# *****************************************************************************
# About original implementation of signal handler
# *****************************************************************************
# ENABLE_TRIGGER_SQL = """
# -- This looks dangerous, but seems to be the recommended approach.
# -- Nevertheless, it looks dangerous, and if for some reason a CASCADE DROP
# --  happens (it should't, but anyway), so, better try some other alternative
# BEGIN;
# DROP TRIGGER IF EXISTS trigger_audit_entry_creator_trigger ON {table_name};
# CREATE TRIGGER trigger_audit_entry_creator_trigger
#     AFTER INSERT OR UPDATE OR DELETE ON {table_name}
#     FOR EACH ROW EXECUTE FUNCTION trigger_audit_entry_creator_func();
#
# COMMIT;
# """
# *****************************************************************************
