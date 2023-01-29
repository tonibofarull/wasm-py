from enum import auto
from enum import Enum


class NumType(Enum):
    i32 = auto()
    i64 = auto()
    f32 = auto()
    f64 = auto()


class VectorType(Enum):
    v128 = auto()


class ReferenceType(Enum):
    funcref = auto()
    externref = auto()


class ValueType(Enum):
    numtype = auto()
    vectype = auto()
    reftype = auto()


class Mut(Enum):
    const = auto()
    var = auto()
