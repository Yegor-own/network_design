from sqlalchemy.orm import Session
from app.models.models import Node, to_geo_point
from app.schemas.node_schema import NodeCreate
from geoalchemy2.functions import ST_X, ST_Y

def get_nodes(db: Session):
    # Вытаскиваем сразу с координатами, чтобы не делать это в API
    return db.query(
        Node.id,
        Node.name,
        ST_Y(Node.location).label("lat"),
        ST_X(Node.location).label("lng"),
    ).all()

def create_node(db: Session, node_in: NodeCreate):
    new_node = Node(
        name=node_in.name,
        location=to_geo_point(node_in.lat, node_in.lng)
    )
    db.add(new_node)
    db.commit()
    db.refresh(new_node)
    return new_node

def get_node_by_name(db: Session, name: str):
    return db.query(Node).filter(Node.name == name).first()