from abc import ABC, abstractmethod
from typing import List, Dict
from v2.src.core.entities import Node, Link, Demand, NetworkParameter, SolverResult

class INodeRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Node]:
        pass
    @abstractmethod
    def create_node(self, name: str, lat: float, lng: float) -> Node:
        pass

class ILinkRepository(ABC):
    @abstractmethod
    def get_all_with_distance(self) -> List[Link]:
        pass

    @abstractmethod
    def get_link_by_id_with_distance(self, link_id: int) -> Link:
        pass

    @abstractmethod
    def create_link(self, node_a_id, node_b_id) -> Link:
        pass

class IDemandRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Demand]:
        pass

    @abstractmethod
    def create_demand(self, source_node_id, dest_node_id, volume) -> Demand:
        pass

class IParamRepository(ABC):
    @abstractmethod
    def get_params_dict(self) -> List[NetworkParameter]:
        pass

    @abstractmethod
    def update_parameter(self, key: str, value: float) -> NetworkParameter:
        pass


class IResultRepository(ABC):
    @abstractmethod
    def save_optimization_result(self, result: SolverResult) -> None:
        pass

    @abstractmethod
    def clear_previous_results(self) -> None:
        pass

    @abstractmethod
    def get_active_links(self):
        pass
    
    @abstractmethod
    def get_all_flows(self):
        pass

class INetworkSolver(ABC):
    @abstractmethod
    def solve(
        self,
        nodes: List[Node],
        links: List[Link],
        demands: List[Demand],
        params: Dict[str, float]
    ) -> SolverResult:
        pass
