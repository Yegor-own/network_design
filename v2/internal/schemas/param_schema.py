from pydantic import BaseModel

class ParameterUpdate(BaseModel):
    value: float
