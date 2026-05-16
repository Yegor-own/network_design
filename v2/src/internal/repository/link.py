from sqlalchemy.orm import Session, aliased
from geoalchemy2.functions import ST_DistanceSphere
from typing import List

from v2.src.core.entities import Link
from v2.src.core.interfaces import ILinkRepository
from v2.src.internal.models.models import CandidateLink, Node

class SqlAlchemyLinkRepository(ILinkRepository):
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_with_distance(self) -> List[Link]:
        NodeA = aliased(Node)
        NodeB = aliased(Node)

        results = self.db.query(
            CandidateLink,
            (ST_DistanceSphere(NodeA.location, NodeB.location) / 1000.0).label("distance")
        ).join(NodeA, CandidateLink.node_a_id == NodeA.id) \
            .join(NodeB, CandidateLink.node_b_id == NodeB.id) \
            .all()
        output = []
        for link, dist in results:
            link.distance = dist
            output.append(link)
        return output
    
    def get_link_by_id_with_distance(self, link_id: int) -> Link:
        NodeA = aliased(Node)
        NodeB = aliased(Node)

        result = self.db.query(
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
    
    def create_link(self, node_a_id, node_b_id) -> Link:
        new_link = CandidateLink(
            node_a_id=node_a_id,
            node_b_id=node_b_id,
        )
        self.db.add(new_link)
        self.db.commit()
        self.db.refresh(new_link)
        return new_link

