from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from v2.core.entities import LinkWithNodes
from v2.internal.db.connect import get_db
from v2.internal.schemas.link_schema import LinkCreate
from v2.internal.repository.link import SqlAlchemyLinkRepository

router = APIRouter()

@router.get("/links", response_model=List[LinkWithNodes])
def get_links(db: Session = Depends(get_db)):
    link_repo = SqlAlchemyLinkRepository(db)
    return link_repo.get_all_with_distance()

@router.get("/links/{link_id}", response_model=LinkWithNodes)
def get_link_by_id(link_id: int, db: Session = Depends(get_db)):
    link_repo = SqlAlchemyLinkRepository(db)
    link = link_repo.get_link_by_id_with_distance(link_id)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return link

@router.post("/links", response_model=LinkWithNodes)
def create_link(link_in: LinkCreate, db: Session = Depends(get_db)):
    link_repo = SqlAlchemyLinkRepository(db)
    return link_repo.create_link(link_in.source_node_id, link_in.dest_node_id)