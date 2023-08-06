import dataclasses
import re
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

import pytest

from django_partitioned_audit import signals
from tests.conftest import skipifadvanced


@dataclasses.dataclass
class ModelClass:
    value: str

    @property
    def _meta(self):
        meta = Mock()
        meta.db_table = self.value
        return meta


class SampleAppConfig:
    name = "app_name"
    trigger_audit_models = ["Model1", "Model2"]
    audit_disabled = ["Model3", "Model4"]


@skipifadvanced
@pytest.mark.django_db(transaction=True)
def test_signals():
    with patch("django_partitioned_audit.signals.connections") as mock_connections:
        mock_execute = MagicMock()
        mock_connections.__getitem__.return_value = MagicMock()
        mock_connections.__getitem__.return_value.cursor.return_value = MagicMock()
        mock_connections.__getitem__.return_value.cursor.return_value.__enter__.return_value = MagicMock()
        mock_connections.__getitem__.return_value.cursor.return_value.__enter__.return_value.execute = mock_execute

        app_config = SampleAppConfig()
        app_config.get_model = Mock(side_effect=lambda arg: ModelClass(value=arg))
        signals.audit_run_post_migrate(app_config, verbosity=0, using="default")

        executed_sql_list = [a_call.args[0].lower() for a_call in mock_execute.call_args_list]

        enabled = [
            re.search(
                r"create trigger trigger_audit_entry_creator_trigger after insert or update or delete on (\S+)", sql
            )
            for sql in executed_sql_list
        ]
        enabled = [_.group(1) for _ in enabled if _]

        disabled = [
            re.search(r"drop trigger if exists trigger_audit_entry_creator_trigger on (\S+);", sql)
            for sql in executed_sql_list
        ]
        disabled = [_.group(1) for _ in disabled if _]

        assert set(enabled) == {"model1", "model2"}
        assert set(disabled) == {"model3", "model4"}
