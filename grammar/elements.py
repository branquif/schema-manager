"""
# Schema Manager elements

Define the elements that compose a schema 

"""

from typing import Dict, List, Tuple, Set, Any, Union
from itertools import chain
from collections import ChainMap
from dataclasses import dataclass, field
from enum import Enum
from data_types import *


class ElTp(Enum):
    USER_TYPE = 1
    SYMBOL = 2
    ENUM = 5
    RECORD = 6
    ATTRIBUTE = 7
    ALIAS = 8
    MODULE = 9
    UNKNOWN = 10

    def __str__(self):
        return self.name.lower()

    def __repr__(self):
        return self.__str__()

@dataclass
class Constant():
    name: str
    value: Any

    def __str__(self):
        return f"const {self.name} = {self.value}"

    def __repr__(self):
        return self.__str__()

class DocType(Enum):
    SIMPLE = 1
    LONG = 2


@dataclass
class Doc:
    doc: str = None
    doc_type: DocType = DocType.SIMPLE

    def __str__(self):
        if self.doc is not None:
            max_print_len = 20
            doc_str = (
                (self.doc[:max_print_len] + "..")
                if len(self.doc) > max_print_len
                else self.doc
            )
            doc_str = doc_str.replace("\n", "\\n").replace("\r", "\\r")
            s = ""
            s += "SDoc(" if self.doc_type == DocType.SIMPLE else ""
            s += "LDoc(" if self.doc_type == DocType.LONG else ""
            return f'{s}"{doc_str}")'
        else:
            return ""

    def __repr__(self):
        return self.__str__()


@dataclass
class Element:
    name: str
    doc: Doc = None
    element_type: ElTp = ElTp.UNKNOWN

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if not isisntance(other, type(self)):
            return NotImplemented
        return self.name == other.name

    def __str__(self):
        s = f"{self.element_type} {self.name}"
        s += f" {self.doc}" if self.doc is not None else ""

        return s

    def __repr__(self):
        return self.__str__()


@dataclass
class UserType(Element):
    element_type: ElTp = ElTp.USER_TYPE
    type: Type = field(default_factory=Type)

    def __str__(self):
        return super().__str__() + f" {self.type}"

    def __repr__(self):
        return self.__str__()


@dataclass
class Symbol(Element):
    element_type: ElTp = ElTp.SYMBOL

    def __hash__(self):
        return super().__hash__()

    def __str__(self):
        s = f"{self.name}"
        s += f" {self.doc}" if self.doc is not None else "-"
        return s


@dataclass
class Enumerator(Element):
    element_type: ElTp = ElTp.ENUM
    symbols: Set[Symbol] = field(default_factory=set)

    def __hash__(self):
        return super().__hash__()

    def __str__(self):
        s = super().__str__() + " : ("
        for sym in self.symbols:
            s += f"{sym}, "
        if ',' in s:
            s = s[:-2]
        s += ")"

        return s

    def __repr__(self):
        return self.__str__()

@dataclass
class Attribute(Element):
    element_type: ElTp = ElTp.ATTRIBUTE

@dataclass
class Record(Element):
    element_type: ElTp = ElTp.RECORD


@dataclass
class Module(Element):
    imports: List = field(default_factory=list)
    element_type: ElTp = ElTp.MODULE
