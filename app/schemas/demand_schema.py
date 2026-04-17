from pydantic import BaseModel

from app.schemas.node_schema import NodeRead


class DemandBase(BaseModel):
    source_node_id: int
    dest_node_id: int
    volume: float

class DemandRead(DemandBase):
    id: int

    class Config:
        from_attributes = True


class DemandReadFull(DemandRead):
    source_node: NodeRead
    dest_node: NodeRead

    class Config:
        from_attributes = True