import io
from io import BytesIO

from wasm_py.values import read_byte
from wasm_py.values import read_u32


def custom_section(stream: BytesIO):
    print("Parsing custom_section")
    size = read_u32(stream)
    stream.seek(size, io.SEEK_CUR)


def resulttype(stream: BytesIO):
    n = read_u32(stream)
    for _ in range(n):
        t = read_byte(stream)
        if t == 0x7F:
            print("i32")
        elif t == 0x7E:
            print("i64")
        elif t == 0x7D:
            print("f32")
        elif t == 0x7C:
            print("f64")
        else:
            raise Exception(f"{hex(t)} is not defined")


def type_section(stream: BytesIO):
    print("Parsing type_section")
    # https://webassembly.github.io/spec/core/binary/types.html#function-types
    size = read_u32(stream)
    print(size)
    n = read_u32(stream)
    print(f"{n=}")
    for i in range(n):
        print(f"function {i}th")
        assert read_byte(stream) == 0x60
        print("input ->")
        resulttype(stream)
        print("output ->")
        resulttype(stream)


def import_section(stream: BytesIO):
    print("Parsing import_section")
    size = read_u32(stream)
    stream.seek(size, io.SEEK_CUR)


def function_section(stream: BytesIO):
    print("Parsing function_section")
    size = read_u32(stream)
    print(size)
    n = read_u32(stream)
    for i in range(n):
        print("funcidx", read_u32(stream))


def table_section(stream: BytesIO):
    print("Parsing table_section")
    size = read_u32(stream)
    print(size)
    stream.seek(size, io.SEEK_CUR)


def memory_section(stream: BytesIO):
    print("Parsing memory_section")
    size = read_u32(stream)
    print(size)
    stream.seek(size, io.SEEK_CUR)


def global_section(stream: BytesIO):
    print("Parsing global_section")
    size = read_u32(stream)
    print(size)
    stream.seek(size, io.SEEK_CUR)


def export_section(stream: BytesIO):
    print("Parsing export_section")
    size = read_u32(stream)
    print(size)
    stream.seek(size, io.SEEK_CUR)


def start_section(stream: BytesIO):
    print("Parsing start_section")
    size = read_u32(stream)
    print(size)
    stream.seek(size, io.SEEK_CUR)


def element_section(stream: BytesIO):
    print("Parsing element_section")
    size = read_u32(stream)
    print(size)
    stream.seek(size, io.SEEK_CUR)


def code_section(stream: BytesIO):
    print("Parsing code_section")
    size = read_u32(stream)
    print(size)
    stream.seek(size, io.SEEK_CUR)


def data_section(stream: BytesIO):
    print("Parsing data_section")
    size = read_u32(stream)
    print(size)
    stream.seek(size, io.SEEK_CUR)


def data_count_section(stream: BytesIO):
    print("Parsing data_count_section")
    size = read_u32(stream)
    print(size)
    stream.seek(size, io.SEEK_CUR)
