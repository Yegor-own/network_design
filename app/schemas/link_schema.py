from pydantic import BaseModel
from app.schemas.node_schema import NodeRead

class CandidateLinkBase(BaseModel):
    node_a_id: int
    node_b_id: int


class CandidateLinkRead(CandidateLinkBase):
    id: int

    class Config:
        from_attributes = True

class CandidateLinkReadFull(CandidateLinkRead):
    node_a: NodeRead
    node_b: NodeRead
    distance: float

    class Config:
        from_attributes = True