"""
Types:
https://webassembly.github.io/spec/core/binary/types.html
"""
import io
import logging
from io import BytesIO

from wasm_py.core.enums import Mut
from wasm_py.core.enums import NumType
from wasm_py.core.enums import ReferenceType
from wasm_py.core.enums import VectorType
from wasm_py.core.models.glob import GlobType
from wasm_py.core.models.table import TableType
from wasm_py.core.models.types.function_type import FunctionType
from wasm_py.core.models.types.limits import Limits
from wasm_py.core.models.types.mem_type import MemType
from wasm_py.core.models.values.number import i32
from wasm_py.parse.utils import selector
from wasm_py.parse.values import read_u32

logger = logging.getLogger(__name__)


def numtype(stream: BytesIO) -> NumType:
    """
    https://webassembly.github.io/spec/core/binary/types.html#number-types
    """
    return selector(
        stream,
        {
            0x7F: NumType.i32,
            0x7E: NumType.i64,
            0x7D: NumType.f32,
            0x7C: NumType.f64,
        },
    )


def vectype(stream: BytesIO) -> VectorType:
    """
    https://webassembly.github.io/spec/core/binary/types.html#vector-types
    """
    return selector(stream, {0x7B: VectorType.v128})


def reftype(stream: BytesIO):
    """
    https://webassembly.github.io/spec/core/binary/types.html#reference-types
    """
    return selector(
        stream,
        {
            0x70: ReferenceType.funcref,
            0x6F: ReferenceType.externref,
        },
    )


def valtype(stream: BytesIO):
    """
    https://webassembly.github.io/spec/core/binary/types.html#value-types
    """
    func = selector(
        stream,
        {
            0x7F: numtype,
            0x5E: numtype,
            0x7D: numtype,
            0x7C: numtype,
            0x7B: vectype,
            0x70: reftype,
            0x6F: reftype,
        },
    )
    stream.seek(-1, io.SEEK_CUR)
    return func(stream)


def resulttype(stream: BytesIO):
    """
    https://webassembly.github.io/spec/core/binary/types.html#result-types
    """
    return [numtype(stream) for _ in range(read_u32(stream))]


def functype(stream: BytesIO):
    """
    https://webassembly.github.io/spec/core/binary/types.html#function-types
    """
    assert read_u32(stream) == 0x60, "Invalid functype flag"
    return FunctionType(inputs=resulttype(stream), outputs=resulttype(stream))


def limits(stream: BytesIO):
    """
    https://webassembly.github.io/spec/core/binary/types.html#limits
    """

    def _limit_unbounded(stream):
        return Limits(min=i32(value=read_u32(stream)), max=None)

    def _limit_bounded(stream):
        return Limits(min=i32(value=read_u32(stream)), max=i32(value=read_u32(stream)))

    func = selector(
        stream,
        {
            0x00: _limit_unbounded,
            0x01: _limit_bounded,
        },
    )
    return func(stream)


def memtype(stream: BytesIO):
    """
    https://webassembly.github.io/spec/core/binary/types.html#memory-types
    """
    return MemType(lim=limits(stream))


def tabletype(stream: BytesIO):
    """
    https://webassembly.github.io/spec/core/binary/types.html#table-types
    """
    return TableType(reftype=reftype(stream), lim=limits(stream))


def mut(stream: BytesIO):
    return selector(
        stream,
        {
            0x00: Mut.const,
            0x01: Mut.var,
        },
    )


def globtype(stream: BytesIO):
    """
    https://webassembly.github.io/spec/core/binary/types.html#global-types
    """
    a = GlobType(valtype=valtype(stream), mut=mut(stream))
    logger.debug(a)
    return a
