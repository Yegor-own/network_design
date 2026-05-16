from pydantic import BaseModel

class LinkCreate(BaseModel):
    source_node_id: int
    dest_node_id: int
