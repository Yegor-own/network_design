from fastapi import APIRouter, Depends, HTTPException
from typing import List

from v2.core.entities import LinkWithNodes
from v2.internal.schemas.link_schema import LinkCreate
from v2.core.services.link_service import LinkService
from v2.internal.handlers.dependencies import get_link_service


router = APIRouter()

@router.get("/links", response_model=List[LinkWithNodes])
def get_links(service: LinkService = Depends(get_link_service)):
    return service.get_all_links_full()

@router.get("/links/{link_id}", response_model=LinkWithNodes)
def get_link_by_id(link_id: int, service: LinkService = Depends(get_link_service)):
    try:
        return service.get_link_by_id_full(link_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/links", response_model=LinkWithNodes)
def create_link(link_in: LinkCreate, service: LinkService = Depends(get_link_service)):
    return service.create_candidate_link(link_in.source_node_id, link_in.dest_node_id) #TODO some error check

@router.delete("/links/{link_id}")
def delete_link(link_id: int, service: LinkService = Depends(get_link_service)):
    status = service.delete_link(link_id)
    if status: 
        return {"status": "ok"}
    else: 
        return {"status": "failed"}