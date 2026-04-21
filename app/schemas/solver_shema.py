from pydantic import BaseModel
from link_schema import CandidateLinkBase
from demand_schema import DemandBase

class SolverNode(BaseModel):
    id: int
    lat: float
    lng: float

class SolverLink(CandidateLinkBase):
    id: int
    distance: float

class SolverDemand(DemandBase):
    id: int