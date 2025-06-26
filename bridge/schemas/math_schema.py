from pydantic import BaseModel

class MathInput(BaseModel):
    a: float
    b: float

class MathResult(BaseModel):
    result: float

class MathError(BaseModel):
    error: str
