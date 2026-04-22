from sqlalchemy.orm import Session
from app.models.models import CandidateLink, Node
from app.schemas.link_schema import CandidateLinkBase
from geoalchemy2.functions import ST_DistanceSphere

def create_link(db: Session, link_in: CandidateLinkBase):
    new_link = CandidateLink(
        node_a_id=link_in.node_a_id,
        node_b_id=link_in.node_b_id,
    )
    db.add(new_link)
    db.commit()
    db.refresh(new_link)
    return new_link

def get_links(db: Session):
    return db.query(CandidateLink).all()

def get_links_with_distance(db: Session):
    return db.query(
        CandidateLink,
        ST_DistanceSphere(Node.location, Node.location).label("distance")
    ).all()

def get_link_by_id_with_distance(db: Session, link_id: int):
    result = db.query(
        CandidateLink,
        ST_DistanceSphere(Node.location, Node.location).label("distance")
    ).filter(CandidateLink.id == link_id).first()
    return result