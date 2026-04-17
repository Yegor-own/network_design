from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from geoalchemy2.functions import ST_X, ST_Y

from app.database import get_db
from app.database import get_db
from app.models.models import CandidateLink, to_geo_point
from app.schemas.candidatelink_schema import CandidateLinkBase, CandidateLinkRead, CandidateLinkReadFull
# from app.api.node_api import router
router = APIRouter()

@router.get("/candidatelinks/{link_id}", response_model=CandidateLinkReadFull)
def get_candidatelink_by_id(link_id: int, db: Session = Depends(get_db)):
    link = db.query(CandidateLink).filter(CandidateLink.id == link_id).first()
    return link

@router.post("/candidatelinks", response_model=CandidateLinkRead)
def create_candidatelink(link_in: CandidateLinkBase, db: Session = Depends(get_db)):
    # existing_link = db.query(CandidateLink).filter(CandidateLink.name == node_in.name).first()
    # if existing_node:
    #     raise HTTPException(status_code=400, detail="Name already registered")

    # 2. Создаем объект модели
    new_link = CandidateLink(
        node_a_id=link_in.node_a_id,
        node_b_id=link_in.node_b_id,
        cost_per_km=link_in.cost_per_km,
        cost_per_unit=link_in.cost_per_unit
    )
    #TODO some processing from brain module
    p_is_active = True
    p_capacity = 0.0
    new_link.is_active = p_is_active
    new_link.capacity = p_capacity

    db.add(new_link)
    db.commit()
    db.refresh(new_link)


    return CandidateLinkRead(
        id=new_link.id,
        node_a_id=new_link.node_a_id,
        node_b_id=new_link.node_b_id,
        cost_per_km=new_link.cost_per_km,
        cost_per_unit=new_link.cost_per_unit,
        is_active=new_link.is_active,
        capacity=new_link.capacity,
    )
