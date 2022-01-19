from enum import Enum


class OperatorEnum(str, Enum):
    contains = "contains"
    notcontains = "notcontains"
    startswith = "startswith"
    endswith = "endswith"
    equals = "equals"
    notequals = "notequals"
