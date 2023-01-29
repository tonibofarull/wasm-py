from pydantic import BaseModel

from wasm_py.core.enums import NumType
from wasm_py.core.enums import ReferenceType
from wasm_py.core.enums import VectorType


class FunctionType(BaseModel):
    inputs: list[NumType | VectorType | ReferenceType]
    outputs: list[NumType | VectorType | ReferenceType]
