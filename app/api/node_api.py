from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from geoalchemy2.functions import ST_X, ST_Y # Функции для вытаскивания координат

from app.database import get_db
from app.models.models import Node, to_geo_point
from app.schemas.node_schema import NodeCreate, NodeRead

router = APIRouter()

@router.get("/nodes", response_model=List[NodeRead])
def get_nodes(db: Session = Depends(get_db)):
    nodes_data = db.query(
        Node.id,
        Node.name,
        ST_Y(Node.location).label("lat"),
        ST_X(Node.location).label("lng"),
    ).all()
    return nodes_data

@router.post("/nodes", response_model=NodeRead)
def create_node(node_in: NodeCreate, db: Session = Depends(get_db)):
    # 1. Проверяем, нет ли узла с таким именем
    existing_node = db.query(Node).filter(Node.name == node_in.name).first()
    if existing_node:
        raise HTTPException(status_code=400, detail="Name already registered")

    # 2. Создаем объект модели
    new_node = Node(
        name=node_in.name,
        location=to_geo_point(node_in.lat, node_in.lng)
    )

    # 3. Сохраняем (Commit)
    db.add(new_node)
    db.commit()
    db.refresh(new_node) # Подтягиваем ID, созданный базой

    # 4. Чтобы вернуть NodeRead, нам нужно обратно вытащить lat/lng из Point
    # В FastAPI это можно сделать так:
    return NodeRead(
        id=new_node.id,
        name=new_node.name,
        lat=node_in.lat,
        lng=node_in.lng
    )