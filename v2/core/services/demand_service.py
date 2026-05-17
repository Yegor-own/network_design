from typing import List
from v2.core.entities import Demand, DemandWithNodes
from v2.core.interfaces import IDemandRepository

class DemandService:
    def __init__(self, demand_repo: IDemandRepository):
        self.demand_repo = demand_repo

    def get_all_demands(self) -> List[Demand]:
        return self.demand_repo.get_all()

    def get_all_demands_full(self) -> List[DemandWithNodes]:
        return self.demand_repo.get_all_full()
    
    def get_demand_by_id_full(self, demand_id: int) -> DemandWithNodes:
        return self.demand_repo.get_demand_by_id_full(demand_id)

    def create_demand(self, source_id: int, dest_id: int, volume: float) -> DemandWithNodes:
        if volume <= 0:
            raise ValueError("Объем трафика должен быть положительным")
        return self.demand_repo.create_demand(source_id, dest_id, volume)

    def delete_demand(self, demand_id: int):
        success = self.demand_repo.delete_demand(demand_id)
        if not success:
            raise ValueError("Требование не найдено")