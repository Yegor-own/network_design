from pydantic import BaseModel, ConfigDict


class ParameterBase(BaseModel):
    key: str
    value: float


class ParameterUpdate(BaseModel):
    value: float


class ParameterRead(ParameterBase):
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)