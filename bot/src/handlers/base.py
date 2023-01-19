from abc import ABC, abstractmethod


class BaseCommand(ABC):
    @classmethod
    @abstractmethod
    def get_handler(cls):
        pass
