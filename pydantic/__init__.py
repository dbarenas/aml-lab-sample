from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


def Field(default: Any = None, **kwargs):
    return default


def validator(*fields):
    def decorator(func: Callable[[Any, Any], Any]):
        return func

    return decorator


class BaseModel:
    def __init__(self, **data: Any) -> None:
        for key, value in data.items():
            setattr(self, key, value)
        self.__post_init__()

    def __post_init__(self) -> None:
        return

    def dict(self):
        return self.__dict__
