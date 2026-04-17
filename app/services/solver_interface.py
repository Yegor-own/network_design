from abc import ABC, abstractmethod
from typing import List, Dict
from pydantic import BaseModel

# --- Схемы данных для обмена (DTO) ---
# Это "чистые" данные, не привязанные к БД (SQLAlchemy)

class SolverNode(BaseModel):
    id: int
    lat: float
    lng: float

class SolverLink(BaseModel):
    id: int
    source_id: int
    target_id: int
    cost_km: float
    cost_unit: float
    distance: float

class SolverDemand(BaseModel):
    id: int
    source_id: int
    dest_id: int
    volume: float  # h_d

class SolverResult(BaseModel):
    # Результат: id линка -> (активен ли z_e, емкость u_e)
    links_results: Dict[int, Dict[str, float]]
    # Потоки x_de (можно усложнить позже)
    flows: List[dict]

# --- САМ ИНТЕРФЕЙС (Аналог interface в Go) ---

class INetworkSolver(ABC):
    @abstractmethod
    def solve(
        self,
        nodes: List[SolverNode],
        links: List[SolverLink],
        demands: List[SolverDemand],
        U_max: float
    ) -> SolverResult:
        """
        Метод должен принять данные сети и вернуть результаты оптимизации.
        Математик реализует этот метод, используя Pyomo.
        """
        pass