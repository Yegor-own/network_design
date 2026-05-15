from abc import ABC, abstractmethod
from typing import List, Dict, Any
from v2.src.core.entities import Node, Link, Demand, SolverResult

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

class IDemandRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Demand]:
        pass

class IParamRepository(ABC):
    @abstractmethod
    def get_params_dict(self) -> Dict[str, float]:
        """Возвращает параметры сети (U, cost_km, cost_u) в виде словаря."""
        pass

class IResultRepository(ABC):
    @abstractmethod
    def save_optimization_result(self, result: SolverResult) -> None:
        """Сохраняет результаты расчета (емкости связей и распределение потоков)."""
        pass

    @abstractmethod
    def clear_previous_results(self) -> None:
        """Удаляет результаты предыдущего расчета."""
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
        """Запускает математическую оптимизацию и возвращает результат."""
        pass
