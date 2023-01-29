from pydantic import BaseModel

from wasm_py.core.models.limits import Limits


class MemoryType(BaseModel):
    lim: Limits
