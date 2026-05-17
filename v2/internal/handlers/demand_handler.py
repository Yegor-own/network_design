from fastapi import APIRouter, Depends
from typing import List

from v2.core.entities import DemandWithNodes
from v2.internal.schemas.demand_schema import DemandCreate
from v2.core.services.demand_service import DemandService
from v2.internal.handlers.dependencies import get_demand_service

router = APIRouter()

@router.get("/demands/{demand_id}", response_model=DemandWithNodes)
def get_demand_by_id(demand_id: int, service: DemandService = Depends(get_demand_service)):
    return service.get_demand_by_id_full(demand_id)

@router.get("/demands", response_model=List[DemandWithNodes])
def get_demands(service: DemandService = Depends(get_demand_service)):
    return service.get_all_demands_full()

@router.post("/demands", response_model=DemandWithNodes)
def create_demand(demand_in: DemandCreate , service: DemandService = Depends(get_demand_service)):
    return service.create_demand(demand_in.source_node_id, demand_in.dest_node_id, demand_in.volume)

@router.delete("/demands/{demand_id}")
def delete_demand(demand_id: int, service: DemandService = Depends(get_demand_service)):
    status = service.delete_demand(demand_id)
    if status: 
        return {"status": "ok"}
    else: 
        return {"status": "failed"}