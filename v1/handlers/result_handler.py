
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from v1.database import get_db
from v1.crud import result as result_crud
from v1.schemas.result_schema import ResultLinkRead, FlowRead

router = APIRouter()

@router.get("/results/links", response_model=List[ResultLinkRead])
def read_active_links(db: Session = Depends(get_db)):
    return result_crud.get_active_links(db)

@router.get("/results/flows", response_model=List[FlowRead])
def read_flows(db: Session = Depends(get_db)):
    return result_crud.get_all_flows(db)