"""
# Schema Manager parser

Parse schema manager definitions and provides an API to interact with the colletion of 
defined items
"""

from itertools import chain
from collections import Iterable
from data_types import *
from elements import *

from lark import Transformer, UnexpectedInput, v_args


@v_args(inline=True)
class ModuleTransformer(Transformer):
    def __init__(self, module_name):
        self._module_name = module_name

    def module_def(self, doc, *imports):
        return self._module_name

    def import_as_name(self, name, *alias):
        if alias:
            return {alias: name}
        else:
            return name

    def import_as_names(self, *aliases):
        return list(chain(aliases))
        # TODO: validate ir alias already exists

    def import_from(self, module, *types):
        ret = None

        if types:
            for t in types:
                if isinstance(t, dict):
                    ret = {}
                    for k, v in types.items():
                        ret[k] = {"module": module, "type": v}
                elif isinstance(t, list):
                    ret = {"module": module, "type": list(chain(t))}
        else:
            ret = {"module": module, "type": "*"}

        return ret

    def import_name(self, module):
        return {"module": module}

    def import_stmt(self, import_stmt):
        return import_stmt

    def module_doc(self, doc):
        return doc
