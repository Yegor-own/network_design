
from fastapi import APIRouter, Depends
from app.handlers import node_handler # Импортируем твою логику

router = APIRouter()

@router.get("/nodes")
def read_nodes():
    # Вызываем функцию из другого файла (хэндлер)
    data = node_handler.get_all_nodes_from_db(db_session=None)
    return data