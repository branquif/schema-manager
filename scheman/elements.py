"""
# Schema Manager elements

Define the elements that compose a schema

"""

from __future__ import annotations

import exceptions as exp
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, List, Optional

from data_types import AllValueType, MinMaxValueType, Type


class ElTp(Enum):

    TYPE = 1
    SYMBOL = 2
    ENUM = 5
    RECORD = 6
    ATTRIBUTE = 7
    ALIAS = 8
    MODULE = 9
    UNKNOWN = 10
    INCLUDE = 11

    def __str__(self) -> str:
        return self.name.lower()

    def __repr__(self):
        return self.__str__()


class Constant(Type):
    def __init__(self, name: str, value: AllValueType):
        self._name = name
        self._value = value

    @property
    def name(self) -> str:
        return self._name

    @property
    def value(self) -> AllValueType:
        return self._value

    def __repr__(self) -> str:
        value = f'"{self._value}"' if isinstance(self._value, str) else self._value
        return f"const {self._name} = {value}"


class Element:
    def __init__(
        self,
        name: str,
        short_doc: Optional[str] = None,
        long_doc: Optional[str] = None,
        element_type: ElTp = ElTp.UNKNOWN,
    ):
        self._name = name
        self._short_doc = short_doc
        self._long_doc = long_doc
        self._element_type = element_type

    @property
    def name(self):
        return self._name

    @property
    def short_doc(self):
        return self._short_doc

    @property
    def long_doc(self):
        return self._long_doc

    @property
    def shorter_short_doc(self):
        if self._short_doc is not None:
            s = f'"{Element._shorter_doc(self._short_doc)}"'
        else:
            s = ""
        return s

    @property
    def shorter_long_doc(self):
        if self._long_doc is not None:
            s = f'LDoc("{Element._shorter_doc(self._long_doc)}")'
        else:
            s = ""
        return s

    @property
    def element_type(self):
        return self._element_type

    @staticmethod
    def _shorter_doc(doc):
        if doc is not None:
            max_print_len = 20
            doc_str = (doc[:max_print_len] + "..",) if len(doc) > max_print_len else doc
            doc_str = doc_str.replace("\n", "\\n").replace("\r", "\\r")
            return doc_str
        else:
            return ""

    def __hash__(self) -> int:
        return hash(self._name)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, type(self)):
            return False
        elif self._name == other.name:
            return True
        else:
            return False

    def __repr__(self) -> str:
        s = f"{self._element_type} {self._name}"
        if self._short_doc is not None:
            s += " " + self.shorter_short_doc
        if self._long_doc is not None:
            s += " " + self.shorter_long_doc
        return s


class UserType(Element):
    def __init__(self, type: Type, **kwargs) -> None:
        self._type = type
        # TODO: need to check if type has been defined in an imported module
        super().__init__(element_type=ElTp.TYPE, **kwargs)

    @property
    def type(self) -> Type:
        return self._type

    def __repr__(self) -> str:
        s = f"type {self._name} {self._type}"
        s += f" {self.shorter_short_doc}"
        s += f" {self.shorter_long_doc}"
        return s


class Symbol(Element):
    def __init__(self, **kwargs) -> None:
        super().__init__(element_type=ElTp.SYMBOL, **kwargs)

    def __hash__(self):
        return super().__hash__()

    def __repr__(self) -> str:
        s = f"{self._name}"
        s += f' "{self.short_doc}"' if self._short_doc is not None else ""
        return s


class Enumerator(Element):
    def __init__(self, **kwargs) -> None:
        self._symbols: List = []
        super().__init__(element_type=ElTp.ENUM, **kwargs)

    def add_symbol(self, symbol: Symbol) -> None:
        if symbol in self._symbols:
            msg = f"Symbol {symbol.name} already declared at enum {self._name}"
            raise exp.DuplicatedElementError(msg)
        else:
            self._symbols.append(symbol)

    def __hash__(self):
        return super().__hash__()

    def __repr__(self) -> str:
        s = super().__repr__() + ": ("
        for sym in self._symbols:
            s += f"{sym}, "
        if "," in s:
            s = s[:-2]
        s += ")"

        return s


class Multiplicity:
    def __init__(
        self, lower_bound: Optional[int] = None, upper_bound: Optional[int] = None
    ) -> None:
        # syntax garantees that if lower bound is set,
        # there is a valid upper bound
        if lower_bound is not None:
            if lower_bound > upper_bound:
                msg = f"Attribute cannot have lower bound multiplicity higher than upper bound"
                raise exp.LowerBoundLargerThanUpperBoundError(msg)
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def __repr__(self):
        s = ""
        if self.lower_bound is not None:
            s += f"({self.lower_bound},{self.upper_bound})"
        elif self.upper_bound is not None:
            s += f"({self.upper_bound})"
        return s


class IncludeAttribute(Element):
    def __init__(self, include_record_name, **kwargs):
        self._include_record_name = include_record_name
        super().__init__(name=include_record_name, element_type=ElTp.INCLUDE, **kwargs)

    @property
    def include_record_name(self):
        return self._include_record_name

    def __repr__(self):
        return f"!{super().__repr__()}"


class Attribute(Element):
    def __init__(
        self,
        type: Type ,
        is_primary_key: bool = False,
        is_discriminator: bool = False,
        discriminator_value: Optional[str] = None,
        multiplicity: Optional[Multiplicity] = None,
        **kwargs,
    ) -> None:
        self._is_primary_key = is_primary_key
        self._is_discriminator = is_discriminator
        self._discriminator_vale = discriminator_value
        self._type = type
        self._multiplicity = multiplicity

        super().__init__(element_type=ElTp.ATTRIBUTE, **kwargs)

    @property
    def is_primary_key(self) -> bool:
        return self._is_primary_key

    @property
    def is_discriminator(self) -> bool:
        return self._is_discriminator

    @property
    def discriminator_value(self) -> Optional[str]:
        return self._discriminator_vale

    @property
    def type(self) -> Type:
        return self._type

    def __repr__(self):
        s = ""
        if self.is_discriminator:
            s += f"%{self.name}"
            if self.discriminator_value is not None:
                s += f' = "{self.discriminator_value}"'
        if self._multiplicity is not None:
            s += f"{self.name} *{self._multiplicity}{self.type}"
        else:
            s += "*" if self.is_primary_key else ""
            s += f"{self.name} {self.type}"
        s += f" {self.shorter_short_doc} {self.shorter_long_doc}"
        return s


@dataclass
class Record(Element):
    element_type: ElTp = ElTp.RECORD
    attributes: List[Element] = field(default_factory=list)
    discriminator_attribute: Optional[Attribute] = None
    parents: List[str] = field(default_factory=list)

    def __repr__(self):
        s = f"record {self.name}"
        s += " :"
        s += f" {self.doc}" if self.doc is not None else ""
        s += "\n"
        for a in self.attributes:
            s += f"\t{a}\n"
        return s


@dataclass
class Module(Element):
    def __init__(self, imports: List, **kwargs) -> None:
        self._imports :List = imports
        super().__init__(element_type=ElTp.MODULE, **kwargs)

    @property
    def imports(self):
        return self._imports
