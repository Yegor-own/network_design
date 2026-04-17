from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.demand_schema import DemandBase, DemandReadFull
from app.crud import demand as demand_crud

router = APIRouter()

@router.get("/demands/{demand_id}", response_model=DemandReadFull)
def get_demand_by_id(demand_id: int, db: Session = Depends(get_db)):
    # return demand_crud.get_demands()
    return None

# @router.post("/links", response_model=CandidateLinkRead)
# def create_link(link_in: CandidateLinkBase, db: Session = Depends(get_db)):
#     return link_crud.create_link(db, link_in)