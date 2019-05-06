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


class ModelTransformer(Transformer):
    def __init__(self, model_name):
        self._model_name = model_name

    def model_def(self, doc, *imports):
        return self._model_name

    def import_as_name(self, name, *alias):
        if alias:
            return {alias: name}
        else:
            return name

    def import_as_names(self, *aliases):
        return list(chain(aliases))
        # TODO: validate ir alias already exists

    def import_from(self, model, *types):
        ret = None

        if types:
            for t in types:
                if isinstance(t, dict):
                    ret = {}
                    for k, v in types.items():
                        ret[k] = {"model": model, "type": v}
                elif isinstance(t, list):
                    ret = {"model": model, "type": list(chain(t))}
        else:
            ret = {"model": model, "type": "*"}

        return ret

    def import_name(self, model):
        return {"model": model}

    def import_stmt(self, import_stmt):
        return import_stmt

    def model_doc(self, doc):
        return doc
