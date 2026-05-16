from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from v2.core.entities import DemandWithNodes
from v2.internal.db.connect import get_db
from v2.internal.schemas.demand_schema import DemandCreate
from v2.internal.repository.demand import SqlAlchemyDemandRepository

router = APIRouter()

@router.get("/demands/{demand_id}", response_model=DemandWithNodes)
def get_demand_by_id(demand_id: int, db: Session = Depends(get_db)):
    demand_repo = SqlAlchemyDemandRepository(db)
    return demand_repo.get_demand_by_id(demand_id)

@router.get("/demands", response_model=List[DemandWithNodes])
def get_demands(db: Session = Depends(get_db)):
    demand_repo = SqlAlchemyDemandRepository(db)
    return demand_repo.get_all()

@router.post("/demands", response_model=DemandWithNodes)
def create_demand(demand_in: DemandCreate ,db: Session = Depends(get_db)):
    demand_repo = SqlAlchemyDemandRepository(db)
    return demand_repo.create_demand(demand_in.source_node_id, demand_in.dest_node_id, demand_in.volume)

@router.delete("/demands/{demand_id}")
def delete_demand(demand_id: int, db: Session = Depends(get_db)):
    demand_repo = SqlAlchemyDemandRepository(db)
    status = demand_repo.delete_demand(demand_id)
    if status: 
        return {"status": "ok"}
    else: 
        return {"status": "failed"}