"""
# Schema Manager parser

Parse schema manager definitions and provides an API to interact with the
colletion of defined items
"""


from lark import Transformer, Tree

from elements import  Enumerator, Symbol
import exceptions as exp
import logging
from utils import NV


class EnumTransformer(Transformer):

    def symbol(self, properties):
        sym_args = {}
        for p in properties:
            if p.data == "symbol_name":
                sym_args["name"] = p.children[0]
            if p.data == "short_doc":
                sym_args["short_doc"] = p.children[0]
        return(Tree("symbol", [Symbol(**sym_args)]))



    def enum_def(self, properties):
        enum_args = {}
        symbols = []
        for p in properties:
            if p.data == "enum_name":
                enum_args["name"] = p.children[0]
            if p.data == "short_doc":
                enum_args["short_doc"] = p.children[0]
            if p.data == "long_doc":
                enum_args["long_doc"] = p.children[0]
            if p.data == "symbol":
                symbols.append(p.children[0])

        enum = Enumerator(**enum_args)
        for symbol in symbols:
            try:
                enum.add_symbol(symbol)
            except exp.DuplicatedElementError as e:
                line = symbol.name.line
                col = symbol.name.column
                message = f"semantic error at ({line}, {col}): "
                message += e.message
                parser_error = exp.SchemanSemanticError(message)
                logging.error(message)

                raise parser_error from e


        return(enum)
