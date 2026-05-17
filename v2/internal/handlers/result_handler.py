
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from v2.internal.db.connect import get_db
from v2.internal.repository.result import SqlAlchemyResultRepository
from v2.internal.schemas.result_schema import ResultLinkRead, FlowRead

router = APIRouter()

@router.get("/results/links", response_model=List[ResultLinkRead])
def read_active_links(db: Session = Depends(get_db)):
    result_repo = SqlAlchemyResultRepository(db)
    return result_repo.get_active_links(db)

@router.get("/results/flows", response_model=List[FlowRead])
def read_flows(db: Session = Depends(get_db)):
    result_repo = SqlAlchemyResultRepository(db)
    return result_repo.get_all_flows(db)