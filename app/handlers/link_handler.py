from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.link_schema import CandidateLinkBase, CandidateLinkRead, CandidateLinkReadFull
from app.crud import link as link_crud

router = APIRouter()

@router.get("/links/{link_id}", response_model=CandidateLinkReadFull)
def get_link_by_id(link_id: int, db: Session = Depends(get_db)):
    return link_crud.get_link_with_distance(db, link_id)

@router.post("/links", response_model=CandidateLinkRead)
def create_link(link_in: CandidateLinkBase, db: Session = Depends(get_db)):
    return link_crud.create_link(db, link_in)

