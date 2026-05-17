from typing import List
from fastapi import APIRouter, Depends, HTTPException

from v2.core.entities import Node
from v2.internal.schemas.node_schema import NodeCreate
from v2.core.services.node_service import NodeService
from v2.internal.handlers.dependencies import get_node_service

router = APIRouter()

@router.get("/nodes", response_model=List[Node])
def get_nodes(service: NodeService = Depends(get_node_service)):
    return service.get_all_nodes()

@router.post("/nodes", response_model=Node)
def create_node(node_in: NodeCreate, service: NodeService = Depends(get_node_service)):
    try:
        return service.create_node(node_in.name, node_in.lat, node_in.lng)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))