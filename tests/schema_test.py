""" base for the schema manager parser """

import sys
from pathlib import Path

from lark import Lark
from lark.indenter import Indenter

# __path__ = os.path.dirname(__file__)

class SchemanIndenter(Indenter):
    NL_type = '_NEWLINE'
    OPEN_PAREN_types = ['LPAR', 'LSQB', 'LBRACE']
    CLOSE_PAREN_types = ['RPAR', 'RSQB', 'RBRACE']
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 8


scheman_lark = Path('./scheman1.lark').read_text()

scheman_parser = Lark(scheman_lark, parser='lalr', postlex=SchemanIndenter())

scheman_type_file = Path('./type_test.schm').read_text()

def test():
    print(scheman_parser.parse(scheman_type_file,).pretty())


if __name__ == '__main__':
    test()
    # scheman_parser.parse(_read(sys.argv[1]) + '\n')
