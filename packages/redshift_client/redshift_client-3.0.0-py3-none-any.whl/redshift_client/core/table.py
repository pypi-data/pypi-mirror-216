from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
    field,
)
from enum import (
    Enum,
)
from fa_purity import (
    Maybe,
)
from fa_purity.frozen import (
    FrozenDict,
    FrozenList,
)
from fa_purity.result import (
    Result,
    ResultE,
)
from redshift_client.core.column import (
    Column,
    ColumnId,
)
from redshift_client.core.data_type.core import (
    DecimalType,
    PrecisionTypes,
    StaticTypes,
)
from redshift_client.utils import (
    NonEmptySet,
)
from typing import (
    Callable,
    FrozenSet,
    TypeVar,
)

_T = TypeVar("_T")


@dataclass(frozen=True)
class _Private:
    pass


@dataclass(frozen=True)
class Table:
    _private: _Private = field(repr=False, hash=False, compare=False)
    order: FrozenList[ColumnId]
    columns: FrozenDict[ColumnId, Column]
    primary_keys: FrozenSet[ColumnId]

    @staticmethod
    def new(
        order: FrozenList[ColumnId],
        columns: FrozenDict[ColumnId, Column],
        primary_keys: FrozenSet[ColumnId],
    ) -> ResultE[Table]:
        in_columns: Callable[[ColumnId], bool] = lambda k: k in columns
        non_duplicated = len(frozenset(order)) == len(order)
        if not non_duplicated:
            return Result.failure(
                Exception("order list must have unique `ColumnId` objs")
            )
        if all(map(in_columns, primary_keys)):
            obj = Table(_Private(), order, columns, primary_keys)
            return Result.success(obj)
        return Result.failure(Exception("All primary keys must be in columns"))


@dataclass(frozen=True)
class BoundColumn:
    "Asserts that the `ColumnId` exists within the bounded table"
    _private: _Private = field(repr=False, hash=False, compare=False)
    table: Table
    column: ColumnId

    @staticmethod
    def new(table: Table, column: ColumnId) -> ResultE[BoundColumn]:
        if column in table.columns:
            return Result.success(BoundColumn(_Private(), table, column))
        return Result.failure(
            Exception(KeyError(f"`{column}` not present in the table"))
        )

    def get_column(self) -> Column:
        return self.table.columns[self.column]


@dataclass(frozen=True)
class ColumnKey:
    "A `BoundColumn` suitable as a distribution or sort key"
    _private: _Private = field(repr=False, hash=False, compare=False)
    column: BoundColumn

    @staticmethod
    def new(column: BoundColumn) -> ResultE[ColumnKey]:
        valid_stc = frozenset(
            {
                StaticTypes.BOOLEAN,
                StaticTypes.REAL,
                StaticTypes.DOUBLE_PRECISION,
                StaticTypes.SMALLINT,
                StaticTypes.INTEGER,
                StaticTypes.BIGINT,
                StaticTypes.DATE,
                StaticTypes.TIME,
                StaticTypes.TIMETZ,
                StaticTypes.TIMESTAMP,
                StaticTypes.TIMESTAMPTZ,
            }
        )
        valid_precision = frozenset(
            {PrecisionTypes.CHAR, PrecisionTypes.VARCHAR}
        )
        valid_type = column.get_column().data_type.map(
            lambda s: s in valid_stc,
            lambda s: s.data_type in valid_precision,
            lambda _: True,
        )
        if valid_type:
            return Result.success(ColumnKey(_Private(), column))
        extract_type = column.get_column().data_type.map(
            lambda s: s,
            lambda s: s.data_type,
            lambda _: DecimalType,
        )
        error = TypeError(
            "The selected column for distribution/sort key has not the expected type. "
            f"i.e. `{extract_type}` is not one of "
            "`BOOLEAN, REAL, DOUBLE PRECISION, SMALLINT, INTEGER, BIGINT, DECIMAL, DATE, TIME, TIMETZ, TIMESTAMP, or TIMESTAMPTZ, CHAR, or VARCHAR`"
        )
        return Result.failure(Exception(error))


class SortKeyType(Enum):
    COMPOUND = "COMPOUND"
    INTERLEAVED = "INTERLEAVED"


@dataclass(frozen=True)
class SortKeys:
    _private: _Private = field(repr=False, hash=False, compare=False)
    _sort_key_type: SortKeyType | None
    _sort_keys: NonEmptySet[ColumnKey] | None

    @staticmethod
    def new(
        sort_key_type: SortKeyType, sort_keys: NonEmptySet[ColumnKey]
    ) -> SortKeys:
        return SortKeys(_Private(), sort_key_type, sort_keys)

    @staticmethod
    def auto() -> SortKeys:
        "Automatic sort key, redshift manages it"
        return SortKeys(_Private(), None, None)

    def map(
        self,
        auto_case: Callable[[], _T],
        specific_case: Callable[[SortKeyType, NonEmptySet[ColumnKey]], _T],
    ) -> _T:
        if self._sort_key_type is None:
            return auto_case()
        if self._sort_keys is not None:
            return specific_case(self._sort_key_type, self._sort_keys)
        raise Exception(
            "[IMPOSSIBLE] private constructor call violation or inner bug."
        )


class DistStyle(Enum):
    AUTO = "AUTO"
    EVEN = "EVEN"
    KEY = "KEY"
    ALL = "ALL"


@dataclass(frozen=True)
class TableAttrs:
    dist_style: DistStyle
    dist_key: Maybe[ColumnKey]
    encode_auto: bool
    sort: SortKeys

    @staticmethod
    def auto() -> TableAttrs:
        return TableAttrs(
            DistStyle.AUTO,
            Maybe.empty(),
            True,
            SortKeys.auto(),
        )


@dataclass(frozen=True)
class ManifestId:
    uri: str
