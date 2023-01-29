"""
Types:
https://webassembly.github.io/spec/core/binary/types.html
"""
import io
import logging
from io import BytesIO
from typing import Any

from wasm_py.core.enums import Mut
from wasm_py.core.enums import NumType
from wasm_py.core.enums import ReferenceType
from wasm_py.core.enums import VectorType
from wasm_py.core.function import FunctionType
from wasm_py.values import read_byte
from wasm_py.values import read_u32

logger = logging.getLogger(__name__)


def _selector(stream: BytesIO, mapping: dict) -> Any:
    byte = read_byte(stream)
    if byte not in mapping:
        raise Exception(f"byte {byte} is not defined")
    res = mapping[byte]
    logger.debug(res)
    return res


def numtype(stream: BytesIO) -> NumType:
    """
    https://webassembly.github.io/spec/core/binary/types.html#number-types
    """
    return _selector(
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
    return _selector(stream, {0x7B: VectorType.v128})


def reftype(stream: BytesIO):
    """
    https://webassembly.github.io/spec/core/binary/types.html#reference-types
    """
    return _selector(
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
    func = _selector(
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
        n = read_u32(stream)
        logger.debug(f"limits: ({n}, any)")
        return n, None

    def _limit_bounded(stream):
        n = read_u32(stream)
        m = read_u32(stream)
        logger.debug(f"limits: ({n}, {m})")
        return n, m

    func = _selector(
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
    limits(stream)


def tabletype(stream: BytesIO):
    """
    https://webassembly.github.io/spec/core/binary/types.html#table-types
    """
    reftype(stream)
    limits(stream)


def mut(stream: BytesIO):
    return _selector(
        stream,
        {
            0x00: Mut.const,
            0x01: Mut.var,
        },
    )


def globaltype(stream: BytesIO):
    """
    https://webassembly.github.io/spec/core/binary/types.html#global-types
    """
    valtype(stream)
    mut(stream)
