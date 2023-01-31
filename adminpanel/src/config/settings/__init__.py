from config import env_manager
from split_settings.tools import include, optional

_base_settings = (
    "components/base.py",
    "components/database.py",
    "components/drf.py",
    # Select the right env:
    "environments/{0}.py".format(env_manager.get_env()),
    # Optionally override some settings:
    optional("environments/local.py"),
)

include(*_base_settings)
