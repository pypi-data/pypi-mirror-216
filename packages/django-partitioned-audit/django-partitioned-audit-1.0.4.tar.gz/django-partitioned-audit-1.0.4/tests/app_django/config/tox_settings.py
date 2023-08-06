import os  # noqa

from .settings import DATABASES  # noqa
from .settings import *  # noqa

# pylint: skip-file

del DATABASES

TOX_ENV_NAME = os.environ["TOX_ENV_NAME"]
py_version, dj_version, pg_version = TOX_ENV_NAME.split("-")

if pg_version == "postgres12":
    from .settings_postgres12 import *  # noqa
elif pg_version == "postgres13":
    from .settings_postgres13 import *  # noqa
elif pg_version == "postgres14":
    from .settings_postgres14 import *  # noqa
elif pg_version == "postgres15":
    from .settings_postgres15 import *  # noqa
else:
    raise NotImplementedError(f"Invalid pg_version={pg_version} - TOX_ENV_NAME={TOX_ENV_NAME}")
