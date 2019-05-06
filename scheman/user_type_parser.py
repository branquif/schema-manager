"""
# Schema Manager parser

Parse schema manager definitions and provides an API to interact with the colletion of
defined items
"""


from collections.abc import Iterable

from lark import Transformer, v_args

from data_types import *
from elements import *


class UserTypeTransformer(Transformer):
    def user_type_def(self, properties):

        user_type_args = {}
        for p in properties:
            if p.data == "user_type_name":
                user_type_args["name"] = p.children[0]
            if p.data == "type" or p.data == "map_type" or p.data == "lst_set_type" or p.data == "union_type":
                user_type_args["type"] = p.children[0]
            if p.data == "short_doc":
                user_type_args["short_doc"] = p.children[0]
            if p.data == "long_doc":
                user_type_args["long_doc"] = p.children[0]

        return UserType(**user_type_args)
