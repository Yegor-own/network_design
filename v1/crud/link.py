from sqlalchemy.orm import Session, aliased
from v1.models.models import CandidateLink, Node
from v1.schemas.link_schema import CandidateLinkBase
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


def get_links_with_distance(db: Session):
    NodeA = aliased(Node)
    NodeB = aliased(Node)

    results = db.query(
        CandidateLink,
        (ST_DistanceSphere(NodeA.location, NodeB.location) / 1000.0).label("distance")
    ).join(NodeA, CandidateLink.node_a_id == NodeA.id) \
        .join(NodeB, CandidateLink.node_b_id == NodeB.id) \
        .all()

    output = []
    for link, dist in results:
        link.distance = dist  # Временно добавляем атрибут
        output.append(link)

    return output


def get_link_by_id_with_distance(db: Session, link_id: int):
    NodeA = aliased(Node)
    NodeB = aliased(Node)

    result = db.query(
        CandidateLink,
        (ST_DistanceSphere(NodeA.location, NodeB.location) / 1000.0).label("distance")
    ).join(NodeA, CandidateLink.node_a_id == NodeA.id) \
        .join(NodeB, CandidateLink.node_b_id == NodeB.id) \
        .filter(CandidateLink.id == link_id).first()

    if result:
        link, dist = result
        link.distance = dist
        return link
    return None