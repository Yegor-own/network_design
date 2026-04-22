from sqlalchemy.orm import Session
from app.models.models import ResultLink
from app.schemas.demand_schema import DemandBase

def create_result_link(db: Session, link_in: ResultLink):
    new_rlink = ResultLink(
        candidate_link_id=link_in.candidate_link_id,
        capacity=link_in.capacity,
    )
    db.add(new_rlink)
    db.commit()
    db.refresh(new_rlink)
    return new_rlink