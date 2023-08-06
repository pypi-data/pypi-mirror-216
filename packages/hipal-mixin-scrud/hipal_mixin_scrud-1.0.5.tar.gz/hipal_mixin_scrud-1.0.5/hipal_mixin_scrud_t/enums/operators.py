from enum import Enum


class Operators(Enum):
    equal = "=="
    ne = "!="
    gte = ">="
    lte = "<="
    gt = ">"
    lt = "<"
    ilike = "ilike"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))
