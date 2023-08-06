import psycopg2

from .settings import *  # noqa

DATABASES = {
    "default": {
        "NAME": "django_partitioned_audit_app",
        "ENGINE": "django.db.backends.postgresql",
        "USER": "test15",
        "PASSWORD": "test15",
        "HOST": "postgres",
        "PORT": 5432,
        "OPTIONS": {
            # THIS IS THE DEFAULT, BUT BETTER BE SPECIFIC
            "isolation_level": psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED,
        },
        "ATOMIC_REQUESTS": True,
    },
}
