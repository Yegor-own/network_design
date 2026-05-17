from fastapi import APIRouter, Depends, HTTPException
from typing import List

from v2.internal.schemas.param_schema import ParameterUpdate
from v2.core.entities import NetworkParameter
from v2.core.services.param_service import ParamService
from v2.internal.handlers.dependencies import get_param_service

router = APIRouter()

@router.get("/parameters", response_model=List[NetworkParameter])
def read_parameters(service: ParamService = Depends(get_param_service)):
    return service.get_all()

@router.patch("/parameters/{key}", response_model=NetworkParameter)
def update_parameter(key: str, param_in: ParameterUpdate, service: ParamService = Depends(get_param_service)):
    try:
        return service.update_parameter(key, param_in.value)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

