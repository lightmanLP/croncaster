from typing import TYPE_CHECKING, TypeVar, overload
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
    cache_path: Path
    tasks: tuple[Cast, ...] = Field(default_factory=tuple)

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
        kwargs["cache_path"] = cache_path
        super().__init__(**kwargs)

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
                with open(dump, "r", encoding="UTF8") as file:
                    return yaml.load(file, yaml.FullLoader) or dict()
            case str():
                return yaml.load(io.StringIO(dump), yaml.FullLoader) or dict()
            case _:
                return dump
