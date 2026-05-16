from fastapi import Depends, APIRouter

from v2.core.services.optimization_service import OptimizationService
from v2.internal.handlers.dependencies import get_optimization_service

router = APIRouter()

@router.post("/calculate", summary="Запустить расчет оптимальной топологии")
def calculate_topology(service: OptimizationService = Depends(get_optimization_service)):
    return service.run_optimization()
