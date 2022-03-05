from enum import Enum

__all__ = ('InputStyle')

class InputStyle(Enum):
    short = 1
    paragraph = 2
    single_line = 1
    multi_line = 2
    long = 2
