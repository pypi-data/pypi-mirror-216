from typing import List

from django.apps import AppConfig


def get_enabled_models(app_config: AppConfig) -> List[str]:
    try:
        trigger_audit_models = app_config.trigger_audit_models
    except AttributeError:
        return []
    return trigger_audit_models


def get_disabled_models(app_config: AppConfig) -> List[str]:
    try:
        trigger_audit_models = app_config.audit_disabled
    except AttributeError:
        return []
    return trigger_audit_models
