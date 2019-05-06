"""
# Schema Manager parser

Parse schema manager definitions and provides an API to interact with the colletion of
defined items
"""

import exceptions as exp
import logging
import pprint
from pathlib import Path

from lark import Lark, Transformer, Tree, UnexpectedInput, v_args
from lark.exceptions import LarkError, VisitError
from lark.indenter import Indenter

from common_parser import *
from const_parser import *
from data_types import *
from elements import *
from enum_parser import *
from module_parser import *
from record_parser import *
from type_parser import *
from user_type_parser import *
from model_parser import *


class SchemanIndenter(Indenter):
    NL_type = "_NEWLINE"
    OPEN_PAREN_types = ["LPAR", "LSQB", "LBRACE"]
    CLOSE_PAREN_types = ["RPAR", "RSQB", "RBRACE"]
    INDENT_type = "_INDENT"
    DEDENT_type = "_DEDENT"
    tab_len = 4


class SchemanTransformer(Transformer):
    pass


logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s", level=logging.DEBUG
)

scheman_grammar = Path("./grammar/scheman.lark").read_text()
parser = Lark(scheman_grammar, parser="lalr", postlex=SchemanIndenter())
module_file = Path("./tests/schemas/type_test.schm")
test_definition = module_file.read_text()
module_name = module_file.stem

parse_tree = parser.parse(test_definition)
print("\n-------------------------------\n")
# print(parse_tree.pretty())
# for t in parse_tree.find_data('record_def'):
#     # print(t)
#     for k in t.children:
#         print(k.data + " : " + str(k))
#         print()
#         if k.data == "attributes":
#             for l in k.children:
#                 print(l.data + " : " + str(l.children))
#                 print()
#         print()
#     print()
# print(parse_tree.children)

try:
    scheman_tree = SchemanTransformer().transform(parse_tree)
        # #         ModuleTransformer(module_name).transform(
        # # RecordTransformer().transform(
        # ConstTransformer().transform(
        #     EnumTransformer().transform(
        #         UserTypeTransformer().transform(
        #             TypeTransformer().transform(
        #                 CommonTransformer().transform(parse_tree)
        #             )
        #         )
        #     )
        # )
        # # )
        # #         )
        # ModelTransformer(module_name).transform(parse_tree)
    # )
    print(scheman_tree.pretty())

except exp.SchemanError:
    pass
