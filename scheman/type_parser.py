"""
# Schema Manager parser

Parse schema manager definitions and provides an API to interact with the colletion of
defined items
"""

from string import Template
import logging

from lark import Transformer, Tree, v_args

from data_types import TypeBuilder
from utils import NV
import exceptions as exp


class TypeTransformer(Transformer):
    def data_type(self, type):
        return type

    def union_type(self, properties) -> Tree:
        type_args = {"name": "union"}
        variants = []
        for p in properties:
            variants.append(p.children[0])
        type_args["variants"] = variants
        t = TypeBuilder.build(**type_args)
        return Tree(data="union_type", children=[t])

    def map_type(self, properties) -> Tree:
        type_args = {}
        for p in properties:
            if p.data == "type_name":
                type_args['name'] = p.children[0]
            if p.data == "is_optional":
                type_args["is_optional"] = True
            if p.data == "type":
                # check if already populated key
                if "key_type" not in type_args:
                    type_args["key_type"] = p.children[0]
                else:
                    type_args["value_type"] = p.children[0]

        t = TypeBuilder.build(**type_args)

        return Tree(data="map_type", children=[t])

    def lst_set_type(self, properties) -> Tree:
        type_args = {}
        for p in properties:
            if p.data == "type_name":
                type_args['name'] = p.children[0]
            if p.data == "is_optional":
                type_args["is_optional"] = True
            if p.data == "type":
                type_args['value_type'] = p.children[0]


        t = TypeBuilder.build(**type_args)

        return Tree(data="lst_set_type", children=[t])

    def type(self, properties) -> Tree:
        type_args = {}
        for p in properties:
            value = p.children[0] if p.children else True
            if p.data == "type_name":
                type_args["name"] = value
            if p.data == "is_optional":
                type_args["is_optional"] = True
            if p.data == "precision_x":
                type_args["precision_x"] = int(value)
            if p.data == "precision_y":
                type_args["precision_y"] = int(value)
            if p.data == "min_value":
                type_args["min_value"] = value
            if p.data == "max_value":
                type_args["max_value"] = value
            if p.data == "default_value":
                type_args["default_value"] = value
        try:
            t = TypeBuilder.build(**type_args)
        except exp.SchemanError as e:
            line = type_args['name'].line
            col = type_args['name'].column
            message = f"Semantic Error at ({line}, {col}): "
            message += e.message
            parser_error = exp.SchemanSemanticError(message)
            logging.error(message)

            raise parser_error from e


        return Tree(data="type", children=[t])
