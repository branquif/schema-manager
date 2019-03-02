""" base for the schema manager parser """

import sys
import pprint

from pathlib import Path

from lark import Lark, UnexpectedInput
from lark.indenter import Indenter

# __path__ = os.path.dirname(__file__)

class SchemanIndenter(Indenter):
    NL_type = '_NEWLINE'
    OPEN_PAREN_types = ['LPAR', 'LSQB', 'LBRACE']
    CLOSE_PAREN_types = ['RPAR', 'RSQB', 'RBRACE']
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 4


scheman_grammar = Path('./grammar/scheman_pure.lark').read_text()

types_schema = Path('./tests/schemas/type_test.schm').read_text()
common_schema = Path('./examples/cash/comum.schm').read_text()
bene_schema = Path('./examples/cash/beneficiario.schm').read_text()
boleto_schema = Path('./examples/cash/boleto.schm').read_text()
imat_common = Path('./examples/imat/imat_common.schm').read_text()
imat = Path('./examples/imat/imat.schm').read_text()

scheman_parser = Lark(scheman_grammar, parser='lalr', postlex=SchemanIndenter())

print("type_test:\n")
print(scheman_parser.parse(types_schema).pretty())
print("\n\n")
print("Common:\n")
print(scheman_parser.parse(common_schema).pretty())
print("\n\n")
print("Beneficiario:\n")
print(scheman_parser.parse(bene_schema).pretty())
print("\n\n")
print("Boleto:\n")
print(scheman_parser.parse(boleto_schema).pretty())
print("\n\n")
print("imat common:\n")
print(scheman_parser.parse(imat_common).pretty())
print("\n\n")
print("imat:\n")
print(scheman_parser.parse(imat).pretty())


