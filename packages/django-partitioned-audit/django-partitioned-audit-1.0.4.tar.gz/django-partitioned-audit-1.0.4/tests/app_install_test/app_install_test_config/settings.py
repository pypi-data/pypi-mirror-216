import psycopg2.extensions

# pylint: skip-file

INSTALLED_APPS = [
    "django.contrib.postgres",
    "django.contrib.contenttypes",
    "django_partitioned_audit",
]

DATABASES = {
    "default": {
        "NAME": "sdist_test_install",
        "ENGINE": "django.db.backends.postgresql",
        "USER": "test15",
        "PASSWORD": "test15",
        "HOST": "localhost",
        "PORT": 55015,
        "OPTIONS": {
            # THIS IS THE DEFAULT, BUT BETTER BE SPECIFIC
            "isolation_level": psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED,
        },
        "ATOMIC_REQUESTS": True,
    },
}
