from pydantic import BaseModel


class DemandCreate(BaseModel):
    source_node_id: int
    dest_node_id: int
    volume: float
