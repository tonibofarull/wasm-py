import io
from io import BytesIO

from wasm_py.parse.sections import code_section
from wasm_py.parse.sections import custom_section
from wasm_py.parse.sections import data_count_section
from wasm_py.parse.sections import data_section
from wasm_py.parse.sections import element_section
from wasm_py.parse.sections import export_section
from wasm_py.parse.sections import function_section
from wasm_py.parse.sections import global_section
from wasm_py.parse.sections import import_section
from wasm_py.parse.sections import memory_section
from wasm_py.parse.sections import read_byte
from wasm_py.parse.sections import start_section
from wasm_py.parse.sections import table_section
from wasm_py.parse.sections import type_section
from wasm_py.utils.parser import get_args


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


def next_section(stream: BytesIO) -> None:
    section = read_byte(stream)
    print(f"section {section}")
    SECTIONS[section](stream)


def parse_wasm(stream: BytesIO):
    stream.seek(0, io.SEEK_END)
    size = stream.tell()
    stream.seek(0)
    assert size >= 8, "Less than 8 bytes"
    check_magic_number(stream.read(4))
    check_version(stream.read(4))
    while stream.tell() < size:
        next_section(stream)


def main():
    args = get_args()
    stream = read_wasm(args.wasm)
    parse_wasm(stream)


if __name__ == "__main__":
    main()
