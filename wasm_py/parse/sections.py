import io
from io import BytesIO

from wasm_py.values import read_byte
from wasm_py.values import read_u32


def custom_section(stream: BytesIO):
    print("Parsing custom_section")
    size = read_u32(stream)
    stream.seek(size, io.SEEK_CUR)
    print("SKIPPED")


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


def reftype(stream: BytesIO):
    byte = read_byte(stream)
    print(byte)
    if byte == 0x70:
        print("funcref")
    elif byte == 0x6F:
        print("externref")
    else:
        raise Exception("Unknown reftpye")


def limits(stream: BytesIO):
    byte = read_byte(stream)
    if byte == 0x00:
        n = read_u32(stream)
        print(f"limits: ({n}, any)")
    elif byte == 0x01:
        n = read_u32(stream)
        m = read_u32(stream)
        print(f"limits: ({n}, {m})")
    else:
        raise Exception("Unknown limits")


def tabletype(stream: BytesIO):
    reftype(stream)
    limits(stream)


def table_section(stream: BytesIO):
    print("Parsing table_section")
    size = read_u32(stream)
    print(size)
    n = read_u32(stream)
    for i in range(n):
        tabletype(stream)


def memtype(stream: BytesIO):
    limits(stream)


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


def mul(stream: BytesIO):
    byte = read_byte(stream)
    if byte == 0x00:
        print("const")
    elif byte == 0x01:
        print("var")
    else:
        raise Exception(f"{hex(byte)} is not defined")


def numtype(stream: BytesIO):
    byte = read_byte(stream)
    if byte == 0x7F:
        print("i32")
    elif byte == 0x7E:
        print("i64")
    elif byte == 0x7D:
        print("f32")
    elif byte == 0x7C:
        print("f64")
    else:
        raise Exception(f"{byte} is not defined")


def vectype(stream: BytesIO):
    byte = read_byte(stream)
    if byte == 0x7B:
        print("v128")
    else:
        raise Exception(f"{hex(byte)} is not defined")


def valtype(stream: BytesIO):
    byte = read_byte(stream)
    print("valtype", hex(byte))
    stream.seek(-1, io.SEEK_CUR)
    if byte in [0x7F, 0x5E, 0x7D, 0x7C]:
        numtype(stream)
    elif byte == 0x7B:
        vectype(stream)
    elif byte in [0x70, 0x6F]:
        reftype(stream)
    else:
        raise Exception("Unknown valtype")


def globaltype(stream: BytesIO):
    valtype(stream)
    mul(stream)


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
