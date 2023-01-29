from pydantic import BaseModel

from wasm_py.core.models.expr import Expr
from wasm_py.core.models.types.glob_type import GlobType


class Glob(BaseModel):
    globtype: GlobType
    expr: Expr
