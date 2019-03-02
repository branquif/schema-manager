"""
# Schema Manager parser

Parse schema manager definitions and provides an API to interact with the colletion of 
defined items
"""

import pprint
from typing import Dict, List, Tuple, Set, Any, Union
from decimal import Decimal
from datetime import date, datetime, time, tzinfo
from itertools import chain
from collections import ChainMap
from dataclasses import dataclass, field
from pathlib import Path
from enum import Enum
from string import Template
from data_types import *
from elements import *

from lark import Lark, Tree, Transformer, Visitor, UnexpectedInput, v_args
from lark.indenter import Indenter


class SchemanIndenter(Indenter):
    NL_type = "_NEWLINE"
    OPEN_PAREN_types = ["LPAR", "LSQB", "LBRACE"]
    CLOSE_PAREN_types = ["RPAR", "RSQB", "RBRACE"]
    INDENT_type = "_INDENT"
    DEDENT_type = "_DEDENT"
    tab_len = 4


def merge_dicts(dicts):
    return {k: v for element in list(dicts) for k, v in element.items()}


@v_args(inline=True)
class SchemanTransformer(Transformer):
    def __init__(self, module_name):
        self.module = Module(name=module_name)

    def multiline_doc(self, doc):
        return Doc(doc[3:-3], DocType.LONG)

    def inline_doc(self, doc):
        return Doc(doc[1:-1], DocType.SIMPLE)

    def dotted_name(self, *args):
        return ".".join(args)

    def dotted_as_name(self, name, *as_name):
        ret = None
        if as_name:
            ret = {as_name: name}
        else:
            ret = name
        return ret

    def dotted_as_names(self, *aliases):
        ret = list(chain(aliases))
        return ret

    def import_as_name(self, name, *alias):
        if alias:
            return {alias: name}
        else:
            return name

    def import_as_names(self, *aliases):
        return list(chain(aliases))
        # TODO: validate ir alias already exists

    def import_from(self, module, *types):
        ret = None

        if types:
            for t in types:
                if isinstance(t, dict):
                    ret = {}
                    for k, v in types.items():
                        ret[k] = {"module": module, "type": v}
                elif isinstance(t, list):
                    ret = {"module": module, "type": list(chain(t))}
        else:
            ret = {"module": module, "type": "*"}

        return ret

    def import_name(self, module):
        return {"module": module}

    def import_stmt(self, import_stmt):
        return import_stmt

    def module_doc(self, doc):
        return doc

    def bool_value(self, value):
        if str(value).upper() == "TRUE":
            return True
        else:
            return False

    def int_value(self, value):
        return int(value)

    def symbol_value(self, value):
        return value

    def string_value(self, value):
        return value[1:-1]

    def decimal_value(self, value):
        return Decimal(value)

    def min_value(self, value):
        return {"min_value": value}

    def max_value(self, value):
        return {"max_value": value}

    def default_value(self, value):
        return {"default_value": value}

    def precision_x(self, value):
        return {"precision_x": int(value)}

    def precision_y(self, value):
        return {"precision_y": int(value)}

    def optional(self):
        return {"opt": True}

    def type_name(self, value):
        return value

    def _get_simple_data_type(self, type_name, prop):
        def get_min_max(prop, min_str, max_str, message):
            min_value = prop.get(min_str, None)
            max_value = prop.get(max_str, None)
            if min_value is not None and max_value is not None:
                if min_value >= max_value:
                    t = Template(message)
                    msg = t.substitute(name=str(type_name), line_num=type_name.line)
                    raise Exception(msg)
            return (min_value, max_value)

        type_name = type_name.lower()
        type = Type(type_name)
        type.type_discriminator = simple_types.get(type_name, DTDisc.GENERIC)

        # optionallity is True as default
        type.is_optional = True if "opt" in prop else False

        type.default_value = prop["default_value"] if "default_value" in prop else None

        if "precision_y" in prop and type_name.lower() == "string":
            (type.min_length, type.max_length) = get_min_max(
                prop,
                "precision_x",
                "precision_y",
                "String min length cannot be bigger than max lengh for type definition $name at line $line_num",
            )

        if "min_value" in prop or "max_value" in prop:
            (type.min_value, type.max_value) = get_min_max(
                prop,
                "min_value",
                "max_value",
                "Min value cannot be bigger than max value for type definition $name at line $line_num",
            )

        if "precision_y" in prop and type_name.lower() == "decimal":
            # decimal uses inverted order
            (type.scale, type.precision) = get_min_max(
                prop,
                "precision_y",
                "precision_x",
                "Decimal scale cannot be bigger than precision for type definition $name at line $line_num",
            )

        return type

    def data_type(self, type):
        return type

    def union_type(self, *types):
        variants = []
        for t in types:
            if isinstance(t, Type):
                variants.append(t)
        return UnionType(name="union", variants=variants)

    def map_type_declaration(self, key_type, value_type) -> MapType:
        return MapType(name="map", key_type=key_type, value_type=value_type)

    def set_type_declaration(self, set_type) -> SetType:
        return SetType(name="set", set_type=set_type)

    def list_type_declaration(self, list_type) -> ListType:
        return ListType(name="list", list_type=list_type)

    def simple_type_declaration(self, type_name, *properties) -> Type:
        prop = merge_dicts(properties)
        return self._get_simple_data_type(type_name, prop)

    def user_type_def(self, user_type_name, *properties):
        doc = None

        for i in properties:
            if isinstance(i, Doc):
                doc = i
            elif isinstance(i, Type) :
                type = i
            else:
                raise Exception(
                    f"User defined type {user_type_name} at line {user_type_name.line} is invalid!"
                )
        user_type = UserType(name=user_type_name, type=type, doc=doc)

        return user_type

    def symbol(self, symbol, *properties):
        # first property, if exists, is the symbol description
        doc = properties[0] if properties else Doc()
        return Symbol(name=symbol, doc=doc)

    def symbols(self, *properties):
        return list(chain(properties))

    def enum_def(self, name, *properties):
        # first property, if exists, is the enum description
        doc = Doc()
        symbols = set()
        for i in properties:
            if isinstance(i, Doc):
                doc = i
            if isinstance(i, list):
                for j in i:
                    symbols.add(j)
        return Enumerator(name=name, symbols=symbols, doc=doc)

    def constant_value(self, value):
        s =f"{value.type} - {value.value} - {value.end_line}"
        print(s)
        return value

    def constant_def(self, name, value):
        return Constant(name=name, value=value)




    def module_def(self, doc, *imports):
        self.module.doc = doc
        self.module.imports = list(chain(imports))
        return self.module


scheman_grammar = Path("./grammar/scheman_pure.lark").read_text()
parser = Lark(scheman_grammar, parser="lalr", postlex=SchemanIndenter())
module_file = Path("./tests/schemas/type_test.schm")
test_definition = module_file.read_text()
module_name = module_file.stem
parse_tree = parser.parse(test_definition)
print("\n\n")
scheman_trans = SchemanTransformer(module_name)
print(scheman_trans.transform(parse_tree).pretty())

# for i, t_item in enumerate(type_names):
#     print(f"name: {type_a0[i]} children: {type_a1[i][0]} "
#           + f"line: {type_a1[i][0].line} col: {type_a1[i][0].column}"
#           + f" type: {type_a1[i][0].type}")
# for item in enums.get_enums():
#    print()
#    pprint.pprint(item)
#    #print(f"{item}")
