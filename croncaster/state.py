from abc import ABC, ABCMeta, abstractmethod

from yamt import SingletonMeta

from .config import Config
from . import tools


class AbstractSingletonMeta(SingletonMeta, ABCMeta):
    ...


class AbstractSingleton(ABC, metaclass=AbstractSingletonMeta):
    ...


class AbstractState(AbstractSingleton):
    @abstractmethod
    def get(self) -> int:
        ...

    @abstractmethod
    def set(self, value: int):
        ...


class State(AbstractState):
    value: int | None = None

    def get(self) -> int:
        if self.value is None:
            b = Config().cache_path.read_bytes()
            if len(b) == 0:
                self.set(0)
            else:
                self.value = tools.to_int(b)
        return self.value

    def set(self, value: int):
        self.value = value
        Config().cache_path.write_bytes(tools.to_bytes(value))
