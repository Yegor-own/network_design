from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.link_schema import CandidateLinkBase, CandidateLinkRead, CandidateLinkReadFull
from app.crud import link as link_crud

router = APIRouter()

@router.get("/links", response_model=List[CandidateLinkReadFull])
def get_all_links(db: Session = Depends(get_db)):
    return link_crud.get_links_with_distance(db)

@router.get("/links/{link_id}", response_model=CandidateLinkReadFull)
def get_link_by_id(link_id: int, db: Session = Depends(get_db)):
    link = link_crud.get_link_by_id_with_distance(db, link_id)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return link

@router.post("/links", response_model=CandidateLinkRead)
def create_link(link_in: CandidateLinkBase, db: Session = Depends(get_db)):
    return link_crud.create_link(db, link_in)