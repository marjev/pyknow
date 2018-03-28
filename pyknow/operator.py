import operator as op
from itertools import chain

from .conditionalelement import ConditionalElement
from .fieldconstraint import P


def from_operator2(o):
    def _from_operator2(b):
        if isinstance(b, ConditionalElement):
            raise TypeError(
                "A ConditionalElement can't be used as an operator condition.")
        else:
            return P(lambda a: o(a, b))
    return _from_operator2


TRUTH = P(bool)
LT = from_operator2(op.lt)
LE = from_operator2(op.le)
EQ = from_operator2(op.eq)
NE = from_operator2(op.ne)
GE = from_operator2(op.ge)
GT = from_operator2(op.gt)
IS = from_operator2(op.is_)
IS_NOT = from_operator2(op.is_not)
CONTAINS = from_operator2(op.contains)


def BETWEEN(a, b):
    """
    The BETWEEN operator selects values within a given range.
    The BETWEEN operator is inclusive: begin and end values are included.

    """
    if any((isinstance(x, ConditionalElement) for x in (a, b))):
        raise TypeError(
            "A ConditionalElement can't be used as an operator condition.")
    else:
        return P(lambda x: a <= x <= b)


class _CALL:
    def __getattr__(self, name):
        def _call(*args, **kwargs):
            if any((isinstance(x, ConditionalElement)
                    for x in chain(args, kwargs.values()))):
                raise TypeError(
                    ("A ConditionalElement can't be used as an "
                     "operator condition."))
            else:
                return P(lambda x: getattr(x, name)(*args, **kwargs))
        return _call

CALL = _CALL()
