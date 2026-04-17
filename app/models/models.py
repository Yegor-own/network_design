from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from geoalchemy2.elements import WKTElement
from app.database import Base  # Базовый класс, от которого все наследуются

def to_geo_point(lat: float, lng: float):
    # ВНИМАНИЕ: В PostGIS порядок обычно (Долгота, Широта) -> (LNG, LAT)
    return WKTElement(f'POINT({lng} {lat})', srid=4326)

class Node(Base):
    __tablename__ = "nodes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    # Геометрия: Точка (Point), SRID 4326 — это стандартные широта/долгота (WGS84)
    # Это позволит Postgres считать расстояние между узлами одной командой
    location = Column(Geometry(geometry_type='POINT', srid=4326))

    # Связи (Relationships) - аналог HasMany в GORM
    # Позволяет удобно доставать все исходящие каналы узла
    outgoing_links = relationship(
        "CandidateLink",
        foreign_keys="CandidateLink.node_a_id",
        back_populates="node_a"
    )

    # Входящие каналы (где этот узел — node_b)
    incoming_links = relationship(
        "CandidateLink",
        foreign_keys="CandidateLink.node_b_id",
        back_populates="node_b"
    )

class CandidateLink(Base):
    __tablename__ = "candidate_links"

    id = Column(Integer, primary_key=True, index=True)
    node_a_id = Column(Integer, ForeignKey("nodes.id"))
    node_b_id = Column(Integer, ForeignKey("nodes.id"))

    cost_per_km = Column(Float)  # c_km из задания
    cost_per_unit = Column(Float)  # c_u из задания

    # Флаг "включен ли канал в решение" (результат работы математика)
    is_active = Column(Boolean, default=False)
    capacity = Column(Float, default=0.0)  # u_e из задания

    node_a = relationship("Node", foreign_keys=[node_a_id], back_populates="outgoing_links")
    node_b = relationship("Node", foreign_keys=[node_b_id], back_populates="incoming_links")


class Demand(Base):
    __tablename__ = "demands"

    id = Column(Integer, primary_key=True, index=True)
    source_node_id = Column(Integer, ForeignKey("nodes.id"))
    dest_node_id = Column(Integer, ForeignKey("nodes.id"))
    volume = Column(Float)  # h_d из задания

    source_node = relationship("Node", foreign_keys=[source_node_id])
    dest_node = relationship("Node", foreign_keys=[dest_node_id])