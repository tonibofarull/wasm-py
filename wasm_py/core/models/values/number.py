import numpy as np
from pydantic import BaseModel
from pydantic import Field

# XXX: improve range checking and usage of 'value' attribute


class i32(BaseModel):
    value: int = Field(..., ge=np.iinfo(np.int32).min, le=np.iinfo(np.int32).max)


class u32(BaseModel):
    value: int = Field(..., ge=np.iinfo(np.uint32).min, le=np.iinfo(np.uint32).max)


class i64(BaseModel):
    value: int = Field(..., ge=np.iinfo(np.int64).min, le=np.iinfo(np.int64).max)


class u64(BaseModel):
    value: int = Field(..., ge=np.iinfo(np.uint64).min, le=np.iinfo(np.uint64).max)


class f32(BaseModel):
    value: float = Field(..., ge=np.finfo(np.float32).min, le=np.finfo(np.float32).max)


class f64(BaseModel):
    value: float = Field(..., ge=np.finfo(np.float64).min, le=np.finfo(np.float64).max)
