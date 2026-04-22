from abc import ABC, abstractmethod
from typing import List, Dict
from pydantic import BaseModel

class SolverNode(BaseModel):
    id: int
    lat: float
    lng: float

    class Config:
        from_attributes = True

class SolverLink(BaseModel):
    id: int
    source_id: int
    target_id: int
    distance: float

    class Config:
        from_attributes = True

class SolverDemand(BaseModel):
    id: int
    source_id: int
    dest_id: int
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
        U_max: float
    ) -> SolverResult:
        pass