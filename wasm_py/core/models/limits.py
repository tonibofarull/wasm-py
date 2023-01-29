from pydantic import BaseModel

from wasm_py.core.models.number import i32


class Limits(BaseModel):
    min: i32
    max: i32 | None
