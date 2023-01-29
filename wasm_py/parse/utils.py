import logging
from io import BytesIO
from typing import Any

from wasm_py.parse.values import read_byte

logger = logging.getLogger(__name__)


def selector(stream: BytesIO, mapping: dict) -> Any:
    byte = read_byte(stream)
    if byte not in mapping:
        raise Exception(f"byte {byte} is not defined")
    res = mapping[byte]
    return res
