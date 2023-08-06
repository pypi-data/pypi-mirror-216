from fa_purity.frozen import (
    FrozenList,
)
from fa_purity.maybe import (
    Maybe,
)
from fa_purity.result import (
    Result,
    ResultE,
)
from fa_purity.utils import (
    raise_exception,
)
from redshift_client.core.column import (
    Column,
    ColumnId,
)
from redshift_client.core.data_type.decode import (
    decode_type,
)
from redshift_client.core.id_objs import (
    Identifier,
)
from redshift_client.sql_client.primitive import (
    PrimitiveVal,
)
from typing import (
    Optional,
    Tuple,
    TypeVar,
)

_T = TypeVar("_T")


def _to_opt(item: _T) -> Optional[_T]:
    return item


def _assert_opt_int(val: PrimitiveVal) -> ResultE[Optional[int]]:
    if isinstance(val, (int, str)):
        try:
            return Result.success(_to_opt(int(val)))
        except ValueError as err:
            return Result.failure(Exception(err))
    if val is None:

        def none() -> Optional[int]:
            return None

        return Result.success(none())
    error = ValueError("not a int|str")
    return Result.failure(Exception(error))


def to_column(raw: FrozenList[PrimitiveVal]) -> Tuple[ColumnId, Column]:
    col = Column(
        decode_type(
            str(raw[2]),
            Maybe.from_optional(
                _assert_opt_int(raw[3]).alt(raise_exception).unwrap()
            ),
            Maybe.from_optional(
                _assert_opt_int(raw[4]).alt(raise_exception).unwrap()
            ),
        ),
        str(raw[5]).upper() == "YES",
        raw[6],
    )
    return (ColumnId(Identifier.new(str(raw[1]))), col)
