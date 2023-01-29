import io
from io import BytesIO

from wasm_py.parse.types import functype
from wasm_py.parse.types import globaltype
from wasm_py.parse.types import memtype
from wasm_py.parse.types import tabletype
from wasm_py.parse.types import valtype
from wasm_py.values import read_byte
from wasm_py.values import read_u32


def validity(func):
    def decorator(stream):
        size = read_u32(stream)
        start_offset = stream.tell()
        res = func(stream)
        assert stream.tell() - start_offset == size, "Invalid section format"
        return res

    return decorator


def custom_section(stream: BytesIO):
    print("Parsing custom_section")
    size = read_u32(stream)
    stream.seek(size, io.SEEK_CUR)
    print("SKIPPED")


@validity
def type_section(stream: BytesIO):
    print("Parsing type_section")
    return [functype(stream) for _ in range(read_u32(stream))]


def import_section(stream: BytesIO):
    print("Parsing import_section")
    size = read_u32(stream)
    stream.seek(size, io.SEEK_CUR)


@validity
def function_section(stream: BytesIO):
    print("Parsing function_section")
    return [read_u32(stream) for _ in range(read_u32(stream))]


def table_section(stream: BytesIO):
    print("Parsing table_section")
    size = read_u32(stream)
    print(size)
    n = read_u32(stream)
    for i in range(n):
        tabletype(stream)


def mem(stream: BytesIO):
    memtype(stream)


def memory_section(stream: BytesIO):
    print("Parsing memory_section")
    size = read_u32(stream)
    print(size)
    n = read_u32(stream)
    for i in range(n):
        mem(stream)


def expr(stream: BytesIO):
    byte = read_byte(stream)
    while byte != 0x0B:
        byte = read_byte(stream)
    # XXX: we are searching for 0x0B but it could be part of a valid instruction.
    print("Finished reading instructions")


def global_section(stream: BytesIO):
    print("Parsing global_section")
    size = read_u32(stream)
    print(size)
    n = read_u32(stream)
    for i in range(n):
        globaltype(stream)
        expr(stream)


def name(stream: BytesIO):
    n = read_u32(stream)
    name = stream.read(n)
    print("name:", str(name))


def exportdesc(stream: BytesIO):
    byte = read_byte(stream)
    if byte == 0x00:
        print("funcidx", read_u32(stream))
    elif byte == 0x01:
        print("tableidx", read_u32(stream))
    elif byte == 0x02:
        print("memidx", read_u32(stream))
    elif byte == 0x03:
        print("globalidx", read_u32(stream))
    else:
        raise Exception("Unknown valtype")


def export_section(stream: BytesIO):
    print("Parsing export_section")
    _ = read_u32(stream)  # size
    n = read_u32(stream)
    for i in range(n):
        name(stream)
        exportdesc(stream)


def start_section(stream: BytesIO):
    print("Parsing start_section")
    size = read_u32(stream)
    print(size)
    stream.seek(size, io.SEEK_CUR)
    print("SKIPPED")


def element_section(stream: BytesIO):
    print("Parsing element_section")
    size = read_u32(stream)
    print(size)
    stream.seek(size, io.SEEK_CUR)


def _locals(stream: BytesIO):
    _ = read_u32(stream)  # n
    valtype(stream)


def func(stream: BytesIO):
    n = read_u32(stream)
    print("locals", n)
    for i in range(n):
        _locals(stream)
    expr(stream)


def code(stream: BytesIO):
    size = read_u32(stream)
    print("size:", size)
    func(stream)


def code_section(stream: BytesIO):
    print("Parsing code_section")
    size = read_u32(stream)
    print(size)
    n = read_u32(stream)
    for i in range(n):
        print(f"Reading code {i}-th")
        code(stream)


def data_section(stream: BytesIO):
    print("Parsing data_section")
    size = read_u32(stream)
    print(size)
    stream.seek(size, io.SEEK_CUR)
    print("SKIPPED")


def data_count_section(stream: BytesIO):
    print("Parsing data_count_section")
    size = read_u32(stream)
    print(size)
    stream.seek(size, io.SEEK_CUR)
    print("SKIPPED")


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
