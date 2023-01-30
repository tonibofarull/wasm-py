from pydantic import BaseModel

from wasm_py.parse.instr_opcode import InstrOpCode


class Expr(BaseModel):
    # XXX: temporal
    val: list[int] | list[InstrOpCode]
