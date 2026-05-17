
from v2.internal.repository import Session, List, ST_X, ST_Y

from v2.core.interfaces import INodeRepository
from v2.core.entities import Node as NodeEntity
from v2.internal.models.models import to_geo_point, Node as NodeModel

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
        return NodeEntity(
            id=new_node.id,
            name=new_node.name,
            lat=lat,
            lng=lng
        )
    
    def get_node_by_name(self, name: str) -> NodeEntity:
        db_node = self.db.query(
            NodeModel.id,
            NodeModel.name,
            ST_Y(NodeModel.location).label("lat"),
            ST_X(NodeModel.location).label("lng")
        ).filter(NodeModel.name == name).first()

        if not db_node:
            return None
        return NodeEntity(
            id=db_node.id,
            name=db_node.name,
            lat=db_node.lat,
            lng=db_node.lng
        )
