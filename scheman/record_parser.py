"""
# Schema Manager parser

Parse schema manager definitions and provides an API to interact with the
colletion of
defined items
"""


from pprint import pprint
import logging
from itertools import chain
from lark import Transformer, Tree, Discard
import exceptions as exp
from data_types import Type

from elements import Attribute, Element, Record, Multiplicity, IncludeAttribute
from utils import NV


class RecordTransformer(Transformer):

    def multiplicity(self, properties):
        multi_args = {}
        line = 0
        col = 0
        for p in properties:
            if p.data == "lower_bound":
                line = p.children[0].line
                col = p.children[0].column
                multi_args['lower_bound'] = int(p.children[0])
            if p.data == "upper_bound":
                multi_args['upper_bound'] = int(p.children[0])
        multi = None
        try:
            multi = Multiplicity(**multi_args)
        except exp.LowerBoundLargerThanUpperBoundError as e:
            message = f"Semantic Error at ({line}, {col}): "
            message += e.message
            parser_error = exp.SchemanSemanticError(message)
            logging.error(message)
            raise parser_error
        return Tree("multiplicity", children=[multi])


    def include_stmt(self, properties):
        args = {}
        line = 0
        col = 0
        for p in properties:
            if p.data == "include_record_name":
                args['include_record_name'] = p.children[0]
            if p.data == "short_doc":
                args['short_doc'] = p.children[0]
            if p.data == 'long_doc':
                args['long_doc'] = p.children[0]
        inc = IncludeAttribute(**args)
        return Tree('include_stmt', children=[inc])


    def attribute(self, properties):
        attr_args = {}
        line = 0
        col = 0
        for p in properties:
            if p.data == "attribute_name":
                line = p.children[0].line
                col = p.children[0].column
                attr_args['name'] = p.children[0]
            if p.data == "primary_key":
                attr_args['is_primary_key'] = True
            if p.data == "attribute_type":
                for at in p.children:
                    if at.data == "multiplicity":
                        attr_args['multiplicity'] = at.children[0]
                    if at.data == "type":
                        attr_args["type"] = at.children[0]
                    if at.data == "short_doc":
                        attr_args['short_doc'] = at.children[0]
                    if at.data == "long_doc":
                        attr_args['long_doc'] = at.children[0]

        attrib = Attribute(**attr_args)
        t = Tree("attribute", children=[attrib])
        return t

    def discriminator_attrib(self, properties):
        attr_args = {"is_discriminator": True}
        for p in properties:
            if p.data == "attribute_name":
                attr_args['name'] = p.children[0]
            if p.data == "discriminator_value":
                attr_args['discriminator_value'] = p.children[0]
            if p.data == "short_doc":
                attr_args['short_doc'] = p.children[0]
            if p.data == "long_doc":
                attr_args['long_doc'] = p.children[0]
        attrib = Attribute(**attr_args)
        t = Tree("attribute", children=[attrib])
        return t



    # def record_def(self, properties):
    #     rec = Record()
    #     for p in properties:
    #         if isinstance(p, Doc):
    #             rec.doc = p
    #         if isinstance(p, list):
    #             rec.attributes = p
    #         if isinstance(p, NV):
    #             rec.__dict__[p.name] = p.value
    #     return rec
