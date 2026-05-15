
from pydantic import BaseModel, ConfigDict


class ResultLinkRead(BaseModel):
    id: int
    candidate_link_id: int
    capacity: float
    node_a_id: int
    node_b_id: int

    model_config = ConfigDict(from_attributes=True)


class FlowRead(BaseModel):
    id: int
    demand_id: int
    link_id: int
    flow_value: float

    model_config = ConfigDict(from_attributes=True)