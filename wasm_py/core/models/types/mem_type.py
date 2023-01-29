from pydantic import BaseModel

from wasm_py.core.models.types.limits import Limits


class MemType(BaseModel):
    lim: Limits
