from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from v2.core.entities import Node
from v2.internal.db.connect import get_db
from v2.internal.schemas.node_schema import NodeCreate
from v2.internal.repository.node import SqlAlchemyNodeRepository

router = APIRouter()

@router.get("/nodes", response_model=List[Node])
def get_nodes(db: Session = Depends(get_db)):
    node_repo = SqlAlchemyNodeRepository(db)
    return node_repo.get_all()

@router.post("/nodes", response_model=Node)
def create_node(node_in: NodeCreate, db: Session = Depends(get_db)):
    node_repo = SqlAlchemyNodeRepository(db)
    if node_repo.get_node_by_name(node_in.name):
        raise HTTPException(status_code=400, detail="Name already registered")

    new_node = node_repo.create_node(node_in.name, node_in.lat, node_in.lng)
    return new_node