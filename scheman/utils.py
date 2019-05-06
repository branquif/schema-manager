from typing import Any, NamedTuple
import logging


def merge_dicts(dicts):
    return {k: v for element in list(dicts) for k, v in element.items()}


class NV(NamedTuple):
    name: str
    value: Any
