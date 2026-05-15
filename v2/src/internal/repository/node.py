from sqlalchemy.orm import Session
from geoalchemy2.functions import ST_X, ST_Y
from typing import List

from v2.src.core.interfaces import INodeRepository
from v2.src.core.entities import Node as NodeEntity
from v2.src.internal.models import to_geo_point, Node as NodeModel
from v2.src.internal.schemas.node_schema import NodeCreate

class SqlAlchemyNodeRepository(INodeRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[NodeEntity]:
        db_nodes = self.db.query(
            NodeModel.id,
            NodeModel.name,
            ST_Y(NodeModel.location).label("lat"),
            ST_X(NodeModel.location).label("lng"),
        ).all()
        
        return [
            NodeEntity(id=n.id, name=n.name, lat=n.lat, lng=n.lng) 
            for n in db_nodes
        ]

    def create_node(self, name: str, lat: float, lng: float) -> NodeEntity:
        new_node = NodeModel(
            name=name,
            location=to_geo_point(lat, lng)
        )
        self.db.add(new_node)
        self.db.commit()
        self.db.refresh(new_node)
        return new_node
