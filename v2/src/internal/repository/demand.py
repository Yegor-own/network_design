from sqlalchemy.orm import Session
from typing import List

from v2.src.core.entities import Demand
from v2.src.core.interfaces import IDemandRepository


class SqlAlchemyDemandRepository(IDemandRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Demand]:
        return self.db.query(
            Demand.id,
            Demand.source_node_id,
            Demand.dest_node_id,
            Demand.volume
        ).all()
    
    def create_demand(self, source_node_id, dest_node_id, volume) -> Demand:
        new_demand = Demand(
            source_node_id=source_node_id,
            dest_node_id=dest_node_id,
            volume=volume
        )
        self.db.add(new_demand)
        self.db.commit()
        self.db.refresh(new_demand)
        return new_demand
