"""
# Schema Manager Types

Define the Data Type classes, simple or complex
"""

from typing import Dict, List, Tuple, Set, Any, Union
from decimal import Decimal
from datetime import date, datetime, time, tzinfo
from dataclasses import dataclass, field
from enum import Enum


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
    GENERIC = 22

    def __str__(self):
        return self.name.lower()

    def __repr__(self):
        return self.__str__()

# map simple types to their type representations
simple_types = {
    "string": DTDisc.STRING,
    "bool": DTDisc.BOOL,
    "int": DTDisc.INT,
    "long": DTDisc.LONG,
    "float": DTDisc.FLOAT,
    "double": DTDisc.DOUBLE,
    "decimal": DTDisc.DECIMAL,
    "uuid": DTDisc.UUID,
    "date": DTDisc.DATE,
    "time": DTDisc.TIME,
    "timetz": DTDisc.TIMETZ,
    "timestamp": DTDisc.TIMESTAMP,
    "timestamptz": DTDisc.TIMESTAMPTZ,
    "blob": DTDisc.BLOB,
}

NumberValueType = Union[int, float, Decimal]
TimeValueType = Union[date, time, datetime]


@dataclass
class Type:
    name: str
    is_optional: bool = True
    type_discriminator: DTDisc = DTDisc.UNKNOWN
    default_value: Any = None
    min_value: Union[NumberValueType, TimeValueType] = None
    max_value: Union[NumberValueType, TimeValueType] = None
    min_length: int = None
    max_length: int = None
    precision: int = None
    scale: int = None

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.name == other.name

    def __repr_(self):
        return self.__str__

    def __str__(self):
        s = f"{self.name}"
        s += "?" if self.is_optional else ""
        if self.default_value is not None:
            s += f" default = "
            if isinstance(self.default_value, str):
                s += f'"{self.default_value}"'
            else:
                s += f"{self.default_value}"
        s += f" min_value = {self.min_value}" if self.min_value is not None else ""
        s += f" max_value = {self.max_value}" if self.max_value is not None else ""
        s += f" min_length = {self.min_length}" if self.min_length is not None else ""
        s += f" max_length = {self.max_length}" if self.max_length is not None else ""
        s += f" precision = {self.precision}" if self.precision is not None else ""
        s += f" scale = {self.scale}" if self.scale is not None else ""
        return s


@dataclass
class MapType(Type):
    type_discriminator: DTDisc = DTDisc.MAP
    key_type: Type = None
    value_type: Type = None

    def __str__(self):
        return f"map({self.key_type}, {self.value_type})"

    def __repr__(self):
        return self.__str__()


@dataclass
class SetType(Type):
    type_discriminator: DTDisc = DTDisc.SET
    set_type: Type = None

    def __str__(self):
        return f"set({self.set_type})"

    def __repr__(self):
        return self.__str__()


@dataclass
class ListType(Type):
    type_discriminator: DTDisc = DTDisc.LIST
    list_type: Type = None

    def __str__(self):
        return f"list({self.list_type})"

    def __repr__(self):
        return self.__str__()


@dataclass
class UnionType(Type):
    type_discriminator: DTDisc = DTDisc.UNION
    variants: List[Type] = field(default_factory=list)

    def __str__(self):
        s = "["
        for v in self.variants:
            s += f"{v}, "
        if "," in s:
            s = s[:-2]
        s += "]"
        return s

    def __repr__(self):
        return self.__str__()


