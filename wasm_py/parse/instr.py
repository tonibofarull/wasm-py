import io
import logging
from io import BytesIO

from wasm_py.parse.instr_opcode import InstrOpCode
from wasm_py.parse.types import valtype
from wasm_py.parse.utils import selector
from wasm_py.parse.values import read_byte
from wasm_py.parse.values import read_s32
from wasm_py.parse.values import read_s33
from wasm_py.parse.values import read_u32

logger = logging.getLogger(__name__)

VARIABLE_INSTR = {InstrOpCode.LOCAL_GET: read_byte}


def blocktype(stream):
    try:
        return valtype(stream)
    except Exception:
        stream.seek(-1, io.SEEK_CUR)
        logger.debug("not valtype")
    x = read_byte(stream)
    if x == 0x40:
        return None
    stream.seek(-1, io.SEEK_CUR)
    logger.debug("reading s33")
    return read_s33(stream)


def if_else_empty(stream):
    logger.debug("Here")
    blocktype(stream)
    instr(stream)


CONTROL_INSTR = {InstrOpCode.IF_ELSE_EMPTY: if_else_empty}


NUMERIC_INSTR = {
    InstrOpCode.I32_CONT: read_s32,
    InstrOpCode.I64_CONT: read_u32,
    InstrOpCode.F32_CONT: read_u32,
    InstrOpCode.F64_CONT: read_u32,
    InstrOpCode.I64_SHR_U: lambda x: 0x66,
    InstrOpCode.I32_ADD: lambda x: 0x66,
}

INSTOPCODE = {x.value: x for x in InstrOpCode}


def instr(stream: BytesIO):
    inst = selector(stream, INSTOPCODE)
    logger.debug(inst)
    if inst in NUMERIC_INSTR:
        _ = NUMERIC_INSTR[inst](stream)
    if inst in CONTROL_INSTR:
        _ = CONTROL_INSTR[inst](stream)
    if inst in VARIABLE_INSTR:
        _ = VARIABLE_INSTR[inst](stream)
    return inst
