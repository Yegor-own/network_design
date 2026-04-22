from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.param_schema import ParameterRead, ParameterUpdate
from app.crud import param as param_crud

router = APIRouter()

@router.get("/parameters", response_model=list[ParameterRead])
def read_parameters(db: Session = Depends(get_db)):
    return param_crud.get_all_params(db)

@router.patch("/parameters", response_model=ParameterRead)
def update_parameter(update_data: ParameterUpdate, db: Session = Depends(get_db)):
    updated_param = param_crud.update_param_by_key(
        db, key=update_data.key, value=update_data.value
    )
    if not updated_param:
        raise HTTPException(status_code=404, detail="Parameter not found")
    return updated_param

