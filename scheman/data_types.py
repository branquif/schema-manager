"""
# Schema Manager Types

Define the Data Type classes, simple or complex
"""

import exceptions as exp
from dataclasses import dataclass, field
from datetime import date, datetime, time
from decimal import Decimal
from enum import Enum
from typing import Any, List, NamedTuple, Optional, Union


class DTDisc(Enum):
    """Data Type Discriminator"""

    UNKNOWN = 0
    BOOL = 1
    INT = 2
    LONG = 3
    FLOAT = 4
    DOUBLE = 5
    DECIMAL = 6
    STRING = 7
    UUID = 8
    DATE = 9
    TIME = 10
    TIMETZ = 11
    TIMESTAMP = 12
    TIMESTAMPTZ = 13
    BLOB = 14
    RECORD = 15
    ENUM = 16
    MAP = 18
    SET = 19
    LIST = 20
    UNION = 21
    CONSTANT = 22
    GENERIC = 23  # need the second pass to expand type from other models

    def __repr__(self):
        return self.name.lower()


# map simple types to their type representations
data_type_discriminators = {
    "string": DTDisc.STRING,
    "text": DTDisc.STRING,
    "varchar": DTDisc.STRING,
    "bool": DTDisc.BOOL,
    "boolean": DTDisc.BOOL,
    "int": DTDisc.INT,
    "integer": DTDisc.INT,
    "long": DTDisc.LONG,
    "float": DTDisc.FLOAT,
    "double": DTDisc.FLOAT,
    "decimal": DTDisc.DECIMAL,
    "number": DTDisc.DECIMAL,
    "uuid": DTDisc.UUID,
    "date": DTDisc.DATE,
    "time": DTDisc.TIME,
    "timetz": DTDisc.TIMETZ,
    "timestamp": DTDisc.TIMESTAMP,
    "datetime": DTDisc.TIMESTAMP,
    "timestamptz": DTDisc.TIMESTAMPTZ,
    "datetimetz": DTDisc.TIMESTAMPTZ,
    "blob": DTDisc.BLOB,
    "map": DTDisc.MAP,
    "set": DTDisc.SET,
    "list": DTDisc.LIST,
    "union": DTDisc.UNION,
    "record": DTDisc.RECORD,
    "enum": DTDisc.ENUM,
}

default_types = {
    DTDisc.STRING,
    DTDisc.BOOL,
    DTDisc.INT,
    DTDisc.LONG,
    DTDisc.FLOAT,
    DTDisc.DECIMAL,
    DTDisc.TIME,
    DTDisc.TIMETZ,
    DTDisc.DATE,
    DTDisc.TIMESTAMP,
    DTDisc.TIMESTAMPTZ,
}

min_max_types = {
    DTDisc.INT,
    DTDisc.LONG,
    DTDisc.DECIMAL,
    DTDisc.FLOAT,
    DTDisc.DATE,
    DTDisc.TIME,
    DTDisc.TIMETZ,
    DTDisc.TIMESTAMP,
    DTDisc.TIMESTAMPTZ,
}

numeric_types = {DTDisc.INT, DTDisc.LONG, DTDisc.FLOAT, DTDisc.DECIMAL}

decimal_precision_limit = 28

NumberValueType = Union[int, float, Decimal]
TimeValueType = Union[date, time, datetime]
AllValueType = Union[str, NumberValueType, TimeValueType]
MinMaxValueType = Union[NumberValueType, TimeValueType]


class Type:
    def __init__(
        self,
        defined_at: Optional[Type],
        model: str,
        name: str,
        type_disc: DTDisc
    ):
        self._defined_at = defined_at
        self._model = model
        self._name = name
        self._type_disc = type_disc

    @property
    def defined_at(self):
        return self._defined_at

    @property
    def model(self):
        return self._model

    @property
    def name(self):
        return self._name

    @property
    def type_disc(self):
        return self._type_disc


class PrimitiveType(Type):
    def __init__(self, is_optional: bool = False) -> None:
        self._is_optional = is_optional

    @property
    def is_optional(self):
        return self._is_optional


class DefaultValueMixin(PrimitiveType):

    def __init__(self, default_value: Optional[AllValueType] = None) -> None:
        self._default_value = default_value

    @property
    def default_value(self):
        return self._default_value


class Blob(PrimitiveType):
    pass


class MinMaxValueMixin:
    def __init__(
        self,
        min_value: Optional[MinMaxValueType] = None,
        max_value: Optional[MinMaxValueType] = None
    ):
        self._min_value = min_value
        self._max_value = max_value

    @classmethod
    def from_xy(
        cls,
        position_x: Optional[MinMaxValueType],
        position_y: Optional[MinMaxValueType],
        ):
        return cls(min_value=position_x, max_value=position_y)

    @classmethod
    def from_y(cls, position_y: Optional[MinMaxValueType]):
        return cls(min_value = None, max_value=position_y)

    @property
    def min_value(self):
        return self._min_value

    @property
    def max_value(self):
        return self._max_value

    @max_value.setter
    def max_value(self, max_value):
        self._max_value = max_value

    @min_value.setter
    def min_value(self, min_value):
        self._min_value = min_value

class DecimalType(DefaultValueMixin, MinMaxValueMixin, PrimitiveType):
    def __init__(self, precision: Optional[int] = None, scale: Optional[int] = None, **kwargs) -> None:
        self._precision = precision
        self._scale = scale
        for k, v in kwargs:
            param = k.lower()
            default_value = v if "default_value" in kwargs else None
            min_value = v if "min_value" in kwargs else None
            max_value = v if "max_value" in kwargs else None
            is_optional = True if "is_optional" in kwargs else False
        DefaultValueMixin.__init__(self, default_value)
        MinMaxValueMixin.__init__(self, min_value, max_value)
        PrimitiveType.__init__(self, is_optional)

    @property
    def precision(self):
        return self._precision

    @property
    def scale(self):
        return self._scale






class Type2:
    def __init__(
        self,
        name: str,
        type_discriminator: Optional[DTDisc] = DTDisc.UNKNOWN,
        is_optional: bool = False,
        default_value: Optional[AllValueType] = None,
        min_value: Optional[MinMaxValueType] = None,
        max_value: Optional[MinMaxValueType] = None,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        precision: Optional[int] = None,
        scale: Optional[int] = None,
    ) -> None:
        self._name = name
        self._is_optional = is_optional
        self._type_discriminator = data_type_discriminators.get(
            name.lower(), DTDisc.UNKNOWN
        )
        self._default_value = default_value
        self._min_value = min_value
        self._max_value = max_value
        self._min_length = min_length
        self._max_length = max_length
        self._precision = precision
        self._scale = scale

        if self._type_discriminator == DTDisc.DECIMAL:
            if scale is not None and scale > precision:
                msg = f"Scale larger than precision for {self._name}"
                raise exp.ScaleLargerThanPrecisionError(msg)
            if precision is not None and precision > decimal_precision_limit:
                msg = f"Precision cannot be larger than {decimal_precision_limit} for {self._name}"
                raise exp.PrecisionOutOfLimitsError(msg)

        if self._type_discriminator == DTDisc.STRING:
            if min_length is not None and min_length >= max_length:
                msg = f"Min length cannot be larger or equal to max lenght for {self._name}"
                raise exp.MinLengthLargerThanMaxError(msg)

        if self._type_discriminator not in min_max_types:
            if self._min_value is not None or self._max_value is not None:
                msg = f"Type {self._name} cannot have min nor max values"
                raise exp.NoMinMaxAllowedError(msg)

        if self._type_discriminator not in default_types:
            if self._default_value is not None:
                msg = f"Type {self._name} cannot have default value"
                raise exp.NoDefaultAllowedError(msg)

    @property
    def name(self) -> str:
        return self._name

    @property
    def is_optional(self) -> bool:
        return self._is_optional

    @property
    def type_discriminator(self):
        return self._type_discriminator

    @property
    def default_value(self) -> Optional[AllValueType]:
        return self._default_value

    @property
    def min_value(self) -> Optional[MinMaxValueType]:
        return self._min_value

    @property
    def max_value(self) -> Optional[MinMaxValueType]:
        return self._max_length

    @property
    def min_length(self) -> Optional[int]:
        return self._min_length

    @property
    def max_length(self) -> Optional[int]:
        return self._max_length

    @property
    def precision(self) -> Optional[int]:
        return self._precision

    @property
    def scale(self) -> Optional[int]:
        return self._scale

    def __hash__(self) -> int:
        return hash(self._name)

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return self._name == other.name

    def __repr__(self) -> str:
        s = f"{self._name}"
        s += "?" if self._is_optional else ""
        if self._type_discriminator == DTDisc.STRING:
            if self._min_length is not None:
                s += f"({self._min_length}, {self._max_length})"
            elif self._max_length is not None:
                s += f"({self._max_length})"
        if self._type_discriminator == DTDisc.DECIMAL:
            if self._scale is not None:
                s += f"({self._precision}, {self._scale})"
            elif self._precision is not None:
                s += f"({self._precision})"
        if self._default_value is not None:
            s += f" default = "
            if isinstance(self._default_value, str):
                s += f'"{self._default_value}"'
            else:
                s += f"{self._default_value}"
        s += f" min = {self._min_value}" if self._min_value is not None else ""
        s += f" max = {self._max_value}" if self._max_value is not None else ""
        return s


class MapType(Type):
    def __init__(
        self,
 name: str,
 key_type: Type,
 value_type: Type,
 is_optional: bool = False
    ) -> None:
        self._name = name
        self._key_type = key_type
        self._value_type = value_type
        self._is_optional = is_optional
        self._type_discriminator = DTDisc.MAP

    @property
    def key_type(self) -> Type:
        return self._key_type

    @property
    def value_type(self) -> Type:
        return self._value_type

    def __repr__(self):
        s = f"{self._name}"
        s += "?" if self._is_optional else ""
        s += f"({self._key_type}, {self._value_type})"
        return s


class SetType(Type):
    def __init__(
self,
 name: str,
 value_type: Type,
 is_optional: bool = False,
) -> None:
        self._name = name
        self._value_type = value_type
        self._is_optional = is_optional
        self._value_type = value_type
        self._type_discriminator = DTDisc.SET

    @property
    def value_type(self) -> Type:
        return self._value_type

    def __repr__(self):
        s = f"{self._name}"
        s += "?" if self._is_optional else ""
        s += f"({self._value_type})"
        return s


class ListType(Type):
    def __init__(
self,
 name: str,
 value_type: Type,
 is_optional: bool = False,
) -> None:
        self._name = name
        self._value_type = value_type
        self._is_optional = is_optional
        self._type_discriminator = DTDisc.LIST

    @property
    def value_type(self) -> Type:
        return self._value_type

    def __repr__(self) -> str:
        s = f"{self._name}"
        s += "?" if self._is_optional else ""
        s += f"({self._value_type})"
        return s


class UnionType(Type):
    def __init__(self, variants: List[Type], **kwargs) -> None:
        self._variants = variants
        kwargs["type_discriminator"] = DTDisc.UNION
        super().__init__(**kwargs)

    @property
    def variants(self) -> List[Type]:
        return self._variants

    def __repr__(self):
        s = "["
        for v in self._variants:
            s += f"{v}, "
        if "," in s:
            s = s[:-2]
        s += "]"
        return s


class TypeBuilder:
    @staticmethod
    def build(**kwargs):
        type_discriminator = data_type_discriminators.get(
            kwargs["name"].lower(), DTDisc.UNKNOWN
        )
        try:
            if type_discriminator == DTDisc.STRING:
                kwargs["max_length"] = kwargs.pop("precision_y", None)
                kwargs["min_length"] = kwargs.pop("precision_x", None)
                type = Type(**kwargs)
            elif type_discriminator == DTDisc.DECIMAL:
                kwargs["scale"] = kwargs.pop("precision_y", None)
                kwargs["precision"] = kwargs.pop("precision_x", None)
                type = Type(**kwargs)
            elif type_discriminator == DTDisc.LIST:
                type = ListType(**kwargs)
            elif type_discriminator == DTDisc.SET:
                type = SetType(**kwargs)
            elif type_discriminator == DTDisc.MAP:
                type = MapType(**kwargs)
            elif type_discriminator == DTDisc.UNION:
                type = UnionType(**kwargs)
            else:
                type = Type(**kwargs)
        except exp.SchemanError as e:
            raise e

        return type
