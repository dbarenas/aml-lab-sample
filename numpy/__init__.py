from __future__ import annotations

import math
from typing import Iterable, List


class NDArray(list):
    @property
    def shape(self):
        if not self:
            return (0,)
        first = self[0]
        if isinstance(first, list):
            return (len(self), len(first))
        return (len(self),)

    def mean(self, axis: int | None = None):
        if axis is None:
            return sum(self) / len(self)
        if axis == 0 and self and isinstance(self[0], list):
            return [sum(column) / len(column) for column in zip(*self)]
        raise NotImplementedError

    def std(self, axis: int | None = None):
        if axis is None:
            m = self.mean()
            variance = sum((v - m) ** 2 for v in self) / len(self)
            return math.sqrt(variance)
        raise NotImplementedError


def array(values: Iterable[float]) -> NDArray:
    return NDArray(values)


def asarray(values: Iterable[Iterable[float]], dtype=float) -> NDArray:
    return NDArray([list(map(dtype, row)) for row in values])


def mean(values: Iterable[float], axis: int | None = None):
    data = NDArray(values) if not isinstance(values, NDArray) else values
    return data.mean(axis=axis)


def std(values: Iterable[float]):
    data = NDArray(values) if not isinstance(values, NDArray) else values
    return data.std()


def vstack(rows: Iterable[Iterable[float]]) -> NDArray:
    return NDArray([list(row) for row in rows])


class FiniteResult(list):
    def all(self):
        return all(bool(item) for item in self)


def isfinite(values: Iterable[float]):
    return FiniteResult(math.isfinite(v) for v in values)


class linalg:
    @staticmethod
    def norm(matrix: Iterable[Iterable[float]], axis: int = 1):
        return [math.sqrt(sum(val * val for val in row)) for row in matrix]


__all__ = [
    "NDArray",
    "array",
    "asarray",
    "mean",
    "std",
    "vstack",
    "isfinite",
    "linalg",
]
