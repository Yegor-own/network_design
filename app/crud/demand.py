from sqlalchemy.orm import Session
from app.models.models import Demand
from app.schemas.demand_schema import DemandBase

def get_demands(db: Session):
    return db.query(
        Demand.id,
        Demand.source_node_id,
        Demand.dest_node_id,
        Demand.volume
    ).all()

def create_demand(db: Session, demand: DemandBase):
    new_demand = Demand(
        source_node_id=demand.source_node_id,
        dest_node_id=demand.dest_node_id,
        volume=demand.volume
    )
    db.add(new_demand)
    db.commit()
    db.refresh(new_demand)
    return new_demand