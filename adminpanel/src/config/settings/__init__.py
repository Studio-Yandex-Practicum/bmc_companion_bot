from dataclasses import dataclass
from os import environ
from typing import Optional

from split_settings.tools import include, optional


@dataclass
class EnvironmentManager:
    DEV_ENVIRONMENT = "development"
    PROD_ENVIRONMENT = "production"
    _env_key = "ENVIRONMENT"

    def set_env(self, env: Optional[str] = None) -> None:
        environ.setdefault(self._env_key, env or self.DEV_ENVIRONMENT)

    def get_env(self) -> str:
        return environ.get(self._env_key, self.DEV_ENVIRONMENT)

    def is_dev(self) -> bool:
        return self.get_env() == self.DEV_ENVIRONMENT

    def is_prod(self) -> bool:
        return self.get_env() == self.PROD_ENVIRONMENT


env_manager = EnvironmentManager()

env_manager.set_env()

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
