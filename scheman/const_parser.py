"""
# Schema Manager parser

Parse schema manager definitions and provides an API to interact with the colletion of 
defined items
"""

from decimal import Decimal
from data_types import *
from elements import *

from lark import Transformer, UnexpectedInput, v_args


@v_args(inline=True)
class ConstTransformer(Transformer):
    def __init__(self):
        self.token_types = {
            "INT": int,
            "DECIMAL": Decimal,
            "BOOL": lambda v: v.lower() == "true",
            "INLINE_STRING": lambda s: s[1:-1],
            "MULTILINE_STRING": lambda s: s[3:-3]
        }


    def constant_value(self, value):
        return self.token_types.get(value.type, value)(value)

    def constant_name(self, name):
        return name

    def constant_def(self, name, value):
        return Constant(name=name, value=value)

