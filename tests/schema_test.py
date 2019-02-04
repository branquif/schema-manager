""" base for the schema manager parser """

import sys
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


scheman_grammar = Path('../grammar/scheman.lark').read_text()

scheman_parser = Lark(scheman_grammar, parser='lalr', postlex=SchemanIndenter())

scheman_file = Path('./schemas/type_test.schm').read_text()


class SchemanSyntaxError(SyntaxError):
    def __str__(self):
        context, line, column = self.args
        return '%s at line %s, column %s.\n\n%s' % (self.label, line, column, context)

class SchemanMissingStringSize(SchemanSyntaxError):
    label = 'String without size'

def error_span(text, pos, span=40):
    start = max(pos - span, 0)
    end = pos + span
    before = text[start:pos].rsplit('\n', 1)[-1]
    after = text[pos:end].split('\n', 1)[0]
    return before + after

def parse(schema_text):
    try:
        return scheman_parser.parse(schema_text)
    except UnexpectedInput as u:
        print(f"syntax error: line: {u.line} col: {u.column}:\n" + u.get_context(schema_text))
        raise


def test():
    print(parse(scheman_file).pretty())


if __name__ == '__main__':
    test()
    # scheman_parser.parse(_read(sys.argv[1]) + '\n')
