from abc import ABC, abstractmethod
from typing import List, Dict
from v2.src.core.entities import Node, LinkWithNodes, DemandWithNodes, NetworkParameter, SolverResult

class INodeRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Node]:
        pass

    @abstractmethod
    def create_node(self, name: str, lat: float, lng: float) -> Node:
        pass

    @abstractmethod
    def get_node_by_name(self, name: str) -> Node:
        pass

class ILinkRepository(ABC):
    @abstractmethod
    def get_all_with_distance(self) -> List[LinkWithNodes]:
        pass

    @abstractmethod
    def get_link_by_id_with_distance(self, link_id: int) -> LinkWithNodes:
        pass

    @abstractmethod
    def create_link(self, source_node_id: int, dest_node_id: int) -> LinkWithNodes:
        pass

class IDemandRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[DemandWithNodes]:
        pass

    @abstractmethod
    def create_demand(self, source_node_id, dest_node_id, volume) -> DemandWithNodes:
        pass

    @abstractmethod
    def get_demand_by_id(self, demand_id: int) -> DemandWithNodes:
        pass

    @abstractmethod
    def delete_demand(self, demand_id) -> bool:
        pass

class IParamRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[NetworkParameter]:
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
