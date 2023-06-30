from typing import TYPE_CHECKING, TypeVar, Iterator, Any, overload
from pathlib import Path
import functools
import math
import io

from pydantic import BaseModel, Extra, Field
from pydantic.main import ModelMetaclass
from pydantic.error_wrappers import ValidationError
from yamt import SingletonMeta
import yaml

if TYPE_CHECKING:
    from typing_extensions import Self

T = TypeVar("T")


class CustomLoader(yaml.FullLoader):
    def include(self, node: yaml.ScalarNode) -> Any:
        with open(self.construct_scalar(node), encoding="UTF-8") as file:
            return yaml.load(file, self.__class__)


CustomLoader.add_constructor("!include", CustomLoader.include)


class ConfigMeta(ModelMetaclass, SingletonMeta):
    ...


class Model(BaseModel):
    __abstract__ = True

    class Config:
        extra = Extra.forbid


class Cast(Model):
    step: int
    command: str


class Config(Model, metaclass=ConfigMeta):
    class Config:
        allow_population_by_field_name = True

    cache_path: Path
    thread_pool_size: int = Field(5)
    unresolved_tasks: tuple[Cast | tuple[Cast, ...], ...] = Field(
        default_factory=tuple,
        alias="tasks"
    )

    def __init__(self, **kwargs) -> None:
        cache_path = kwargs.get("cache_path")
        match cache_path:
            case str():
                cache_path = Path(cache_path)
            case Path():
                ...
            case None:
                cache_path = Path.cwd() / "croncaster.cache"
            case _:
                raise ValidationError()
        cache_path.touch(exist_ok=True)
        kwargs["cache_path"] = cache_path.resolve()
        super().__init__(**kwargs)

    @property
    def tasks(self) -> Iterator[Cast]:
        for i in self.unresolved_tasks:
            if isinstance(i, tuple):
                yield from i
            else:
                yield i

    @property
    def max(self) -> int:
        nums = tuple(i.step for i in Config().tasks)
        if len(nums) == 1:
            return nums[0]
        else:
            return (
                functools.reduce(lambda x, y: x * y, nums)
                // math.gcd(*nums)
            )

    @classmethod
    def from_dump(cls, dump: dict | Path | str) -> "Self":
        assert isinstance(dump, (dict, str, Path))
        return cls(**cls.read_dump(dump))

    @overload
    @staticmethod
    def read_dump(dump: str | Path) -> dict:
        ...

    @overload
    @staticmethod
    def read_dump(dump: T) -> T:
        ...

    @staticmethod
    def read_dump(dump: T) -> dict | T:
        match dump:
            case Path():
                assert dump.exists() and dump.is_file()
                with open(dump, "r", encoding="UTF-8") as file:
                    return yaml.load(file, CustomLoader) or dict()
            case str():
                return yaml.load(io.StringIO(dump), CustomLoader) or dict()
            case _:
                return dump

    @classmethod
    def wipe(cls):
        cls._wipe_singleton()
