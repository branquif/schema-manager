""" schema manager exceptions """

from typing import Optional


class SchemanError(Exception):
    """base class for exceptions in schema manager"""

    def __init__(
        self,
        message: Optional[str] = None,
        element_name: Optional[str] = None,
        type_name: Optional[str] = None,
        line: Optional[int] = None,
    ) -> None:
        if message is None:
            msg = ""
            element_line = 0
            type_line = 0
            if element_name is not None:
                msg += f"element: {element_name} "
            if type_name is not None:
                msg += f"type: {type_name} "
            if hasattr(type_name, "line"):
                type_line = type_name.line
            if hasattr(element_name, "line"):
                element_line = element_name.line
            if line is None:
                if element_line > 0:
                    line = element_line
                elif type_line > 0:
                    line = type_line
            elif line > 0:
                msg += f" line: {line}"
            self.message = msg
        else:
            self.message = message
        super().__init__(self.message)
        self.type_name = type_name
        self.element_name = element_name
        self.line = line

    def __str__(self):
        return self.message


class DuplicatedElementError(SchemanError):
    """Exception raised for not allowed duplicated elements."""


class NoDefaultTypeError(SchemanError):
    """Raised when the type has no default"""


class NoMinMaxTypeError(SchemanError):
    """Raised when the type has no Min nor Max values"""


class ScaleLargerThanPrecisionError(SchemanError):
    """Decimal type scale larger than precision"""

class PrecisionOutOfLimitsError(SchemanError):
    """Decimal type out of decimal limits"""

class MinLengthLargerThanMaxError(SchemanError):
    """String min length equal or larger than max length"""

class LowerBoundLargerThanUpperBoundError(SchemanError):
    """multiplicity lower bound bigger thatn upper bound"""

class MaxLengthStringError(SchemanError):
    """String max length larger than limit"""

class NoDefaultAllowedError(SchemanError):
    """type should not have default values"""

class NoMinMaxAllowedError(SchemanError):
    """type should not have min nor max values"""


class SchemanSemanticError(SchemanError):
    """Any error that occured during parsing"""

