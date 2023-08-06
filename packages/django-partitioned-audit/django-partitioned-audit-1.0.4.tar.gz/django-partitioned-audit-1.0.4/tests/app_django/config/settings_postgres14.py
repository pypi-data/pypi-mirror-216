import psycopg2.extensions

DATABASES = {
    "default": {
        "NAME": "django_partitioned_audit_app",
        "ENGINE": "django.db.backends.postgresql",
        "USER": "test14",
        "PASSWORD": "test14",
        "HOST": "localhost",
        "PORT": 55014,
        "OPTIONS": {
            # THIS IS THE DEFAULT, BUT BETTER BE SPECIFIC
            "isolation_level": psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED,
        },
        "ATOMIC_REQUESTS": True,
    },
}
