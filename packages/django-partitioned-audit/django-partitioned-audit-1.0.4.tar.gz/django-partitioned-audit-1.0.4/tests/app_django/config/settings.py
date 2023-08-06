import os

from .settings_boilerplate import *  # noqa

# pylint: skip-file

DEBUG = True

if "DPA_AUDIT_TABLE_MANAGER" in os.environ:
    DPA_AUDIT_TABLE_MANAGER = os.environ["DPA_AUDIT_TABLE_MANAGER"]

INSTALLED_APPS = [
    # Django applications
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    # django partitioned audit & test applications
    "django_partitioned_audit",
    "app.apps.AppConfig",
    "second_app.apps.SecondaryAppConfig",
]

# By default, let's import some db configuration, to make sure it will work
# when using this file directly

from .settings_postgres15 import *  # noqa
