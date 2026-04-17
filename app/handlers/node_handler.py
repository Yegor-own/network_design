from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.node_schema import NodeCreate, NodeRead
from app.crud import node as node_crud

router = APIRouter()

@router.get("/nodes", response_model=List[NodeRead])
def get_nodes(db: Session = Depends(get_db)):
    return node_crud.get_nodes(db)

@router.post("/nodes", response_model=NodeRead)
def create_node(node_in: NodeCreate, db: Session = Depends(get_db)):
    # Проверка бизнес-логики
    if node_crud.get_node_by_name(db, node_in.name):
        raise HTTPException(status_code=400, detail="Name already registered")

    # Вызов CRUD
    new_node = node_crud.create_node(db, node_in)

    # Мапим обратно для ответа (т.к. в БД лежит Geometry, а нам нужны lat/lng)
    return NodeRead(
        id=new_node.id,
        name=new_node.name,
        lat=node_in.lat,
        lng=node_in.lng
    )