from sqlalchemy.orm import Session
from app.models.models import CandidateLink, Node
from app.schemas.link_schema import CandidateLinkBase
from geoalchemy2.functions import ST_DistanceSphere

def create_link(db: Session, link_in: CandidateLinkBase):
    new_link = CandidateLink(
        node_a_id=link_in.node_a_id,
        node_b_id=link_in.node_b_id,
        cost_per_km=link_in.cost_per_km,
        cost_per_unit=link_in.cost_per_unit,
        is_active=False,
        capacity=0.0
    )
    db.add(new_link)
    db.commit()
    db.refresh(new_link)
    return new_link

def get_link_with_distance(db: Session, link_id: int):
    # Пример того, как через PostGIS вытащить расстояние в метрах между узлами
    # ST_DistanceSphere считает расстояние по сфере (земному шару)
    result = db.query(
        CandidateLink,
        ST_DistanceSphere(Node.location, Node.location).label("dist_meters")
        # Тут нужна будет более сложная связка (join) для корректного расчета
    ).filter(CandidateLink.id == link_id).first()
    return result