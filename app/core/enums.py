from enum import IntEnum

class ValueType(IntEnum):
    STRING = 1
    INTEGER = 2
    FLOAT = 3
    BOOLEAN = 4
    DATETIME = 5
    UUID = 6
    JSON = 7