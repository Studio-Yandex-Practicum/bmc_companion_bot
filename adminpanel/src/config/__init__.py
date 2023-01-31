from dataclasses import dataclass
from os import environ
from typing import Optional


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
