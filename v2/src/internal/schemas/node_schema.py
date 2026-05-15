from pydantic import BaseModel

class NodeCreate(BaseModel):
    name: str
    lat: float
    lng: float

class NodeRead(BaseModel):
    id: int
    name: str
    lat: float
    lng: float

    class Config:
        from_attributes = True