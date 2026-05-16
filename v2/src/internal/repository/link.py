from sqlalchemy.orm import Session, aliased
from geoalchemy2.functions import ST_DistanceSphere
from typing import List

from v2.src.core.entities import Node, Link, LinkWithNodes
from v2.src.core.interfaces import ILinkRepository
from v2.src.internal.models.models import CandidateLink, Node as NodeModel

class SqlAlchemyLinkRepository(ILinkRepository):
    def __init__(self, db: Session):
        self.db = db

    def sql_to_linkwithnodes(row) -> LinkWithNodes:
        link, dist, src, dst = row
        src_node = Node(
            id=src.id,
            name=src.name,
            lat=src.lat,
            lng=src.lng
        )
        dst_node = Node(
            id=dst.id,
            name=dst.name,
            lat=dst.lat,
            lng=dst.lng
        )
        return LinkWithNodes(
            link.id,
            source_node=src_node,
            dest_node=dst_node,
            distance=dist
        )
    
    def get_all_with_distance(self) -> List[LinkWithNodes]:
        Source = aliased(NodeModel)
        Dest = aliased(NodeModel)

        results = self.db.query(
            CandidateLink,
            (ST_DistanceSphere(Source.location, Dest.location) / 1000.0).label("distance"),
            Source,
            Dest
        ).join(Source, CandidateLink.source_node_id == Source.id) \
            .join(Dest, CandidateLink.dest_node_id == Dest.id) \
            .all()
        
        links: List[LinkWithNodes] = []
        for row in results:
            link =  self.sql_to_linkwithnodes(row)
            links.append(link)
        return links
    
    def get_link_by_id_with_distance(self, link_id: int) -> LinkWithNodes:
        Source = aliased(NodeModel)
        Dest = aliased(NodeModel)

        result = self.db.query(
            CandidateLink,
            (ST_DistanceSphere(Source.location, Dest.location) / 1000.0).label("distance"),
            Source,
            Dest
        ).join(Source, CandidateLink.source_node_id == Source.id) \
            .join(Dest, CandidateLink.dest_node_id == Dest.id) \
            .filter(CandidateLink.id == link_id).first()
        
        if result:
            return self.sql_to_linkwithnodes(result)
        return None
    
    def create_link(self, source_node_id: int, dest_node_id: int) -> Link:
        new_link = CandidateLink(
            source_node_id=source_node_id,
            dest_node_id=dest_node_id,
        )
        self.db.add(new_link)
        self.db.commit()
        self.db.refresh(new_link)

        Source = aliased(NodeModel)
        Dest = aliased(NodeModel)

        result = self.db.query(
            CandidateLink,
            (ST_DistanceSphere(Source.location, Dest.location) / 1000.0).label("distance"),
            Source,
            Dest
        ).join(Source, CandidateLink.source_node_id == Source.id) \
            .join(Dest, CandidateLink.dest_node_id == Dest.id) \
            .filter(CandidateLink.id == new_link.id).first()
        
        return self.sql_to_linkwithnodes(result)