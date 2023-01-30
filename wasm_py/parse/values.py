import logging
from io import BytesIO


logger = logging.getLogger(__name__)


def read_byte(stream: BytesIO) -> int:
    return stream.read(1)[0]


def read_u32(stream: BytesIO) -> int:
    # XXX: apply LEB128
    return stream.read(1)[0]


def read_leb128(stream: BytesIO) -> int:
    val = 0
    logger.debug("Reading LEB128")
    while True:
        byte = read_byte(stream)
        val = val << 8
        val += byte & ~128
        logger.debug(f"{val=} {hex(byte)=}")
        if (byte & 128) == 0:
            break
    return val


def read_s32(stream: BytesIO) -> int:
    # XXX: apply LEB128
    return read_leb128(stream)


def read_s33(stream: BytesIO) -> int:
    logger.debug("here")
    return read_leb128(stream)
