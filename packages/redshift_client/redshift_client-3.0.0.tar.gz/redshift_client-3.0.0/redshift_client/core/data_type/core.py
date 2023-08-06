# ref https://docs.aws.amazon.com/redshift/latest/dg/c_Supported_data_types.html

from dataclasses import (
    dataclass,
)
from enum import (
    Enum,
)
from typing import (
    Callable,
    TypeVar,
    Union,
)

_T = TypeVar("_T")


class StaticTypes(Enum):
    SMALLINT = "SMALLINT"
    INTEGER = "INTEGER"
    BIGINT = "BIGINT"
    REAL = "REAL"
    DOUBLE_PRECISION = "DOUBLE PRECISION"
    BOOLEAN = "BOOLEAN"
    DATE = "DATE"
    TIMESTAMP = "TIMESTAMP"
    TIMESTAMPTZ = "TIMESTAMPTZ"
    TIME = "TIME"
    TIMETZ = "TIMETZ"
    GEOMETRY = "GEOMETRY"
    GEOGRAPHY = "GEOGRAPHY"
    HLLSKETCH = "HLLSKETCH"
    SUPER = "SUPER"


class PrecisionTypes(Enum):
    CHAR = "CHAR"
    VARCHAR = "VARCHAR"
    VARBYTE = "VARBYTE"


class ScaleTypes(Enum):
    DECIMAL = "DECIMAL"


@dataclass(frozen=True)
class NonStcDataTypes:
    value: Union[PrecisionTypes, ScaleTypes]


@dataclass(frozen=True)
class PrecisionType:
    data_type: PrecisionTypes
    precision: int


@dataclass(frozen=True)
class DecimalType:
    precision: int
    scale: int


@dataclass(frozen=True)
class DataType:
    _value: Union[StaticTypes, PrecisionType, DecimalType]

    def map(
        self,
        static_case: Callable[[StaticTypes], _T],
        precision_case: Callable[[PrecisionType], _T],
        decimal_case: Callable[[DecimalType], _T],
    ) -> _T:
        if isinstance(self._value, StaticTypes):
            return static_case(self._value)
        if isinstance(self._value, PrecisionType):
            return precision_case(self._value)
        return decimal_case(self._value)
