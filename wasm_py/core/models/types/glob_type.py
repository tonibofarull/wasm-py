from pydantic import BaseModel

from wasm_py.core.enums import Mut
from wasm_py.core.enums import NumType
from wasm_py.core.enums import ReferenceType
from wasm_py.core.enums import VectorType


class GlobType(BaseModel):
    valtype: NumType | VectorType | ReferenceType
    mut: Mut
