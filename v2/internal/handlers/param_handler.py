from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from v2.internal.db.connect import get_db
from v2.core.entities import NetworkParameter
from v2.internal.repository.param import SqlAlchemyParamRepository

router = APIRouter()

@router.get("/parameters", response_model=List[NetworkParameter])
def read_parameters(db: Session = Depends(get_db)):
    param_repo = SqlAlchemyParamRepository(db)
    return param_repo.get_all()

@router.patch("/parameters/{key}", response_model=NetworkParameter)
def update_parameter(key: str, value: float, db: Session = Depends(get_db)):
    param_repo = SqlAlchemyParamRepository(db)
    updated = param_repo.update_parameter(key, value)
    if not updated:
        raise HTTPException(status_code=404, detail="Parameter not found")
    return updated

