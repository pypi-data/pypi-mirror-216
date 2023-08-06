from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
    field,
)
from fa_purity.result import (
    Result,
    ResultE,
)
from typing import (
    FrozenSet,
    Generic,
    TypeVar,
)

_T = TypeVar("_T")


@dataclass(frozen=True)
class _Private:
    pass


@dataclass(frozen=True)
class NonEmptySet(Generic[_T]):
    _private: _Private = field(repr=False, hash=False, compare=False)
    _inner: FrozenSet[_T]

    @staticmethod
    def new(item: _T) -> NonEmptySet[_T]:
        return NonEmptySet(_Private(), frozenset([item]))

    @staticmethod
    def from_set(items: FrozenSet[_T]) -> ResultE[NonEmptySet[_T]]:
        if items != frozenset([]):
            return Result.success(NonEmptySet(_Private(), frozenset(items)))
        error = ValueError("`FrozenSet` must not be empty.")
        return Result.failure(Exception(error))

    def to_set(self) -> FrozenSet[_T]:
        return self._inner

    def __contains__(self, item: _T) -> bool:
        return item in self._inner
