from pydantic import BaseModel

from wasm_py.core.enums import ReferenceType
from wasm_py.core.models.limits import Limits


class TableType(BaseModel):
    reftype: ReferenceType
    lim: Limits
