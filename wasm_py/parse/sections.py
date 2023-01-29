import io
import logging
from io import BytesIO

from wasm_py.core.models.glob import Expr
from wasm_py.core.models.glob import Glob
from wasm_py.core.module import Module
from wasm_py.parse.types import functype
from wasm_py.parse.types import globtype
from wasm_py.parse.types import memtype
from wasm_py.parse.types import tabletype
from wasm_py.parse.types import valtype
from wasm_py.parse.utils import selector
from wasm_py.parse.values import read_byte
from wasm_py.parse.values import read_u32

logger = logging.getLogger(__name__)


def validity(func):
    def decorator(stream, module):
        size = read_u32(stream)
        start_offset = stream.tell()
        func(stream, module)
        assert stream.tell() - start_offset == size, "Invalid section format"

    return decorator


def custom_section(stream: BytesIO, module: Module):
    logger.debug("Parsing custom_section")
    size = read_u32(stream)
    stream.seek(size, io.SEEK_CUR)
    logger.debug("SKIPPED")


@validity
def type_section(stream: BytesIO, module: Module) -> None:
    logger.debug("Parsing type_section")
    module.set_types([functype(stream) for _ in range(read_u32(stream))])


def import_section(stream: BytesIO, module: Module):
    logger.debug("Parsing import_section")
    size = read_u32(stream)
    stream.seek(size, io.SEEK_CUR)


@validity
def function_section(stream: BytesIO, module: Module) -> None:
    logger.debug("Parsing function_section")
    module.set_type_indices([read_u32(stream) for _ in range(read_u32(stream))])


@validity
def table_section(stream: BytesIO, module: Module):
    logger.debug("Parsing table_section")
    module.set_tables([tabletype(stream) for _ in range(read_u32(stream))])


@validity
def memory_section(stream: BytesIO, module: Module):
    logger.debug("Parsing memory_section")
    module.set_memory([memtype(stream) for _ in range(read_u32(stream))])


def expr(stream: BytesIO):
    byte = read_byte(stream)
    while byte != 0x0B:
        byte = read_byte(stream)
    # XXX: we are searching for 0x0B but it could be part of a valid instruction.
    logger.debug("Finished reading instructions")
    return Expr(val=None)


@validity
def global_section(stream: BytesIO, module: Module):
    logger.debug("Parsing global_section")
    # TODO: implement
    module.set_memory(
        [
            Glob(globtype=globtype(stream), expr=expr(stream))
            for _ in range(read_u32(stream))
        ]
    )


def exportdesc(stream: BytesIO):
    func = selector(
        stream,
        {
            0x00: lambda: logger.debug(f"funcidx {read_u32(stream)}"),
            0x01: lambda: logger.debug(f"tableidx {read_u32(stream)}"),
            0x02: lambda: logger.debug(f"memidx {read_u32(stream)}"),
            0x03: lambda: logger.debug(f"globalidx {read_u32(stream)}"),
        },
    )
    func()


def export_section(stream: BytesIO, module: Module):
    logger.debug("Parsing export_section")
    _ = read_u32(stream)  # size
    n = read_u32(stream)

    def name(stream: BytesIO):
        n = read_u32(stream)
        name = stream.read(n)
        logger.debug(f"name: {str(name)}")

    for i in range(n):
        name(stream)
        exportdesc(stream)


def start_section(stream: BytesIO, module: Module):
    logger.debug("Parsing start_section")
    size = read_u32(stream)
    logger.debug(size)
    stream.seek(size, io.SEEK_CUR)
    logger.debug("SKIPPED")


def element_section(stream: BytesIO, module: Module):
    logger.debug("Parsing element_section")
    size = read_u32(stream)
    logger.debug(size)
    stream.seek(size, io.SEEK_CUR)


def _locals(stream: BytesIO):
    _ = read_u32(stream)  # n
    valtype(stream)


def func(stream: BytesIO):
    n = read_u32(stream)
    logger.debug(f"locals {n}")
    for i in range(n):
        _locals(stream)
    expr(stream)


def code(stream: BytesIO):
    size = read_u32(stream)
    logger.debug(f"size: {size}")
    func(stream)


def code_section(stream: BytesIO, module: Module):
    logger.debug("Parsing code_section")
    size = read_u32(stream)
    logger.debug(size)
    n = read_u32(stream)
    for i in range(n):
        logger.debug(f"Reading code {i}-th")
        code(stream)


def data_section(stream: BytesIO, module: Module):
    logger.debug("Parsing data_section")
    size = read_u32(stream)
    logger.debug(size)
    stream.seek(size, io.SEEK_CUR)
    logger.debug("SKIPPED")


def data_count_section(stream: BytesIO, module: Module):
    logger.debug("Parsing data_count_section")
    size = read_u32(stream)
    logger.debug(size)
    stream.seek(size, io.SEEK_CUR)
    logger.debug("SKIPPED")


SECTIONS = {
    0: custom_section,
    1: type_section,
    2: import_section,
    3: function_section,
    4: table_section,
    5: memory_section,
    6: global_section,
    7: export_section,
    8: start_section,
    9: element_section,
    10: code_section,
    11: data_section,
    12: data_count_section,
}
