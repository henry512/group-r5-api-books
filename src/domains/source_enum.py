from enum import Enum


class SourceEnum(str, Enum):
    internal = "internal"
    external = "external"
