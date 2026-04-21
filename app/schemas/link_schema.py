from pydantic import BaseModel
from app.schemas.node_schema import NodeRead

class CandidateLinkBase(BaseModel):
    node_a_id: int
    node_b_id: int

    cost_per_km: float
    cost_per_km: float


class CandidateLinkRead(CandidateLinkBase):
    id: int
    is_active: bool
    capacity: float

    class Config:
        from_attributes = True

class CandidateLinkReadFull(CandidateLinkRead):
    node_a: NodeRead
    node_b: NodeRead

    class Config:
        from_attributes = True