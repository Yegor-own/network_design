from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from typing import List
from app.database import get_db
from app.schemas.demand_schema import DemandBase, DemandReadFull, DemandRead
from app.crud import demand as demand_crud

router = APIRouter()

@router.get("/demands/{demand_id}", response_model=DemandReadFull)
def get_demand_by_id(demand_id: int, db: Session = Depends(get_db)):
    # return demand_crud.get_demands()
    return None

@router.get("/demands", response_model=List[DemandRead])
def get_demands(db: Session = Depends(get_db)):
    return demand_crud.get_demands(db)

@router.post("/demands", response_model=DemandRead)
def create_demand(demand_in: DemandBase ,db: Session = Depends(get_db)):
    return demand_crud.create_demand(db, demand_in)

@router.delete("/demands/{demand_id}")
def delete_demand(demand_id: int, db: Session = Depends(get_db)):
    # TODO delete demand
    return {"status": "ok"}