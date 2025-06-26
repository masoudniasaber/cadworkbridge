from pydantic import BaseModel

class SpellcheckResponse(BaseModel):
    corrections: str

class SpellcheckError(BaseModel):
    error: str
