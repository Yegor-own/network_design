
from fastapi import APIRouter, Depends
from typing import List

from v2.core.entities import ResultLink, FlowAssignment, SolverResult, NetworkCost
from v2.core.services.optimization_service import OptimizationService
from v2.internal.handlers.dependencies import get_optimization_service

router = APIRouter()

@router.post("/calculate", summary="Запустить расчет оптимальной топологии")
def calculate_topology(service: OptimizationService = Depends(get_optimization_service)):
    return service.run_optimization()

@router.get("/results/all", response_model=SolverResult)
def get_solver_results(service: OptimizationService = Depends(get_optimization_service)):
    return service.get_results()

@router.get("/results/links", response_model=List[ResultLink])
def get_result_links(service: OptimizationService = Depends(get_optimization_service)):
    return service.get_result_links()

@router.get("/results/flows", response_model=List[FlowAssignment])
def get_flows(service: OptimizationService = Depends(get_optimization_service)):
    return service.get_flows()

@router.get("/cost", response_model=NetworkCost)
def get_total_cost(service: OptimizationService = Depends(get_optimization_service)):
    return service.get_total_cost()