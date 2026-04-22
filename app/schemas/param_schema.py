from pydantic import BaseModel


class ParameterUpdate(BaseModel):
    key: str
    value: float


class ParameterRead(ParameterUpdate):
    description: str | None = None

    class Config:
        from_attributes = True