"""
# Schema Manager parser

Parse schema manager definitions and provides an API to interact with the colletion of 
defined items
"""

from decimal import Decimal
from itertools import chain
from data_types import *
from elements import *

from lark import Transformer, UnexpectedInput, Tree, v_args


@v_args(inline=True)
class CommonTransformer(Transformer):
    def long_doc(self, doc):
        return Tree(data="long_doc", children=[doc[3:-3]])

    def short_doc(self, doc):
        return Tree(data="short_doc", children=[doc[1:-1]])

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
