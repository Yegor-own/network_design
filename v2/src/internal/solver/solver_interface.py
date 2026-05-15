from abc import ABC, abstractmethod
from typing import List, Dict
from pydantic import BaseModel, Field


class SolverNode(BaseModel):
    id: int
    lat: float
    lng: float

    class Config:
        from_attributes = True

class SolverLink(BaseModel):
    id: int
    source_id: int = Field(validation_alias="node_a_id")
    target_id: int = Field(validation_alias="node_b_id")
    distance: float

    class Config:
        from_attributes = True

class SolverDemand(BaseModel):
    id: int
    source_id: int = Field(validation_alias="source_node_id")
    dest_id: int = Field(validation_alias="dest_node_id")
    volume: float  # h_d

    class Config:
        from_attributes = True

class SolverResult(BaseModel):
    links_results: Dict[int, Dict[str, float]]
    flows: List[dict]


class INetworkSolver(ABC):
    @abstractmethod
    def solve(
        self,
        nodes: List[SolverNode],
        links: List[SolverLink],
        demands: List[SolverDemand],
        U_max: float,
        cost_km: float,
        cost_u: float
    ) -> SolverResult:
        pass