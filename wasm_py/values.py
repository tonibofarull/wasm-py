from io import BytesIO


def read_byte(stream: BytesIO) -> int:
    return stream.read(1)[0]


def read_u32(stream: BytesIO) -> int:
    # XXX: apply LEB128
    return stream.read(1)[0]
