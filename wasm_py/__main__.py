import io
import logging
from io import BytesIO

from wasm_py.core.module import Module
from wasm_py.parse.sections import SECTIONS
from wasm_py.parse.values import read_byte
from wasm_py.utils.parser import get_args

logger = logging.getLogger(__name__)


def read_wasm(fp: str) -> BytesIO:
    with open(fp, "rb") as f:
        return BytesIO(f.read())


# https://webassembly.github.io/spec/core/binary/modules.html#binary-module
# Magic number: 0x00 0x61 0x73 0x6D that corresponds to "\0asm"
def check_magic_number(magic: bytes) -> None:
    assert magic == b"\x00asm", "Wrong magic number"


# Version
def check_version(version: bytes) -> None:
    assert version == b"\x01\x00\x00\x00"


def next_section(stream: BytesIO, module: Module) -> None:
    section = read_byte(stream)
    logger.debug(
        f"############################ Section {section} ############################"
    )
    size = read_byte(stream)
    cont = stream.read(size)
    logger.debug(f"{section=}, {size=}, {cont=}")
    stream.seek(-size-1, io.SEEK_CUR)
    SECTIONS[section](stream, module)


def parse_wasm(stream: BytesIO) -> Module:
    stream.seek(0, io.SEEK_END)
    size = stream.tell()
    stream.seek(0)
    assert size >= 8, "Less than 8 bytes"
    check_magic_number(stream.read(4))
    check_version(stream.read(4))
    module = Module()
    while stream.tell() < size:
        next_section(stream, module)
    return module


def main():
    args = get_args()
    logging.basicConfig(
        level=logging.getLevelName(args.level),
        format="%(levelname)s [%(filename)13s:%(lineno)-3s]  %(message)s",
        datefmt="%Y-%m-%d:%H:%M:%S",
    )
    stream = read_wasm(args.wasm)
    parse_wasm(stream)


if __name__ == "__main__":
    main()
