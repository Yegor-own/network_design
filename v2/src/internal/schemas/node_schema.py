from pydantic import BaseModel

class NodeCreate(BaseModel):
    name: str
    lat: float
    lng: float