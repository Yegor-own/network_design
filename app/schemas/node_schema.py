from pydantic import BaseModel
from typing import Optional

# Базовая схема для получения данных от фронтенда
class NodeCreate(BaseModel):
    name: str
    lat: float
    lng: float

# Схема для отдачи данных фронтенду (то, что пойдет в JSON)
class NodeRead(BaseModel):
    id: int
    name: str
    lat: float
    lng: float

    # Важно: это позволяет Pydantic читать данные прямо из объектов SQLAlchemy
    class Config:
        from_attributes = True