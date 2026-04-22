from sqlalchemy.orm import Session, aliased
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


def get_links_with_distance(db: Session):
    # Создаем алиасы для узлов
    NodeA = aliased(Node)
    NodeB = aliased(Node)

    # Строим запрос с двумя Join-ами
    results = db.query(
        CandidateLink,
        # Делим на 1000, так как ST_DistanceSphere возвращает метры, а нам нужны КМ (по ТЗ)
        (ST_DistanceSphere(NodeA.location, NodeB.location) / 1000.0).label("distance")
    ).join(NodeA, CandidateLink.node_a_id == NodeA.id) \
        .join(NodeB, CandidateLink.node_b_id == NodeB.id) \
        .all()

    # Мапим результат (CandidateLink, distance) в один объект для Pydantic
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