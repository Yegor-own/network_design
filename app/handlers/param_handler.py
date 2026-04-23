from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.param_schema import ParameterRead, ParameterUpdate
from app.crud import param as param_crud

router = APIRouter()

@router.get("/parameters", response_model=list[ParameterRead])
def read_parameters(db: Session = Depends(get_db)):
    return param_crud.get_all_params(db)

@router.patch("/parameters/{key}", response_model=ParameterRead)
def update_parameter(key: str, param_in: ParameterUpdate, db: Session = Depends(get_db)):
    updated = param_crud.update_parameter(db, key, param_in.value)
    if not updated:
        raise HTTPException(status_code=404, detail="Parameter not found")
    return updated

