from enum import Enum


class InstrOpCode(Enum):
    END = 0x0B

    I32_CONT = 0x41
    I64_CONT = 0x42
    F32_CONT = 0x43
    F64_CONT = 0x44
    I32_ADD = 0x6A

    I64_SHR_U = 0x88

    IF_ELSE_EMPTY = 0x04

    LOCAL_GET = 0x20
