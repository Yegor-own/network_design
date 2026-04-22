from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from geoalchemy2.elements import WKTElement
from app.database import Base

def to_geo_point(lat: float, lng: float):
    return WKTElement(f'POINT({lng} {lat})', srid=4326)

class Node(Base):
    __tablename__ = "nodes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    location = Column(Geometry(geometry_type='POINT', srid=4326))

    outgoing_links = relationship("CandidateLink", foreign_keys="[CandidateLink.node_a_id]", back_populates="node_a")
    incoming_links = relationship("CandidateLink", foreign_keys="[CandidateLink.node_b_id]", back_populates="node_b")
    demands_as_source = relationship("Demand", foreign_keys="[Demand.source_node_id]", back_populates="source_node")
    demands_as_dest = relationship("Demand", foreign_keys="[Demand.dest_node_id]", back_populates="dest_node")

class CandidateLink(Base):
    __tablename__ = "candidate_links"

    id = Column(Integer, primary_key=True, index=True)
    node_a_id = Column(Integer, ForeignKey("nodes.id"))
    node_b_id = Column(Integer, ForeignKey("nodes.id"))

    node_a = relationship("Node", foreign_keys=[node_a_id], back_populates="outgoing_links")
    node_b = relationship("Node", foreign_keys=[node_b_id], back_populates="incoming_links")
    result_link = relationship("ResultLink", foreign_keys="[ResultLink.candidate_link_id]", back_populates="candidate_link")
    flows = relationship("FlowAssignment", foreign_keys="[FlowAssignment.link_id]", back_populates="link")


class Demand(Base):
    __tablename__ = "demands"

    id = Column(Integer, primary_key=True, index=True)
    source_node_id = Column(Integer, ForeignKey("nodes.id"))
    dest_node_id = Column(Integer, ForeignKey("nodes.id"))
    volume = Column(Float)  # h_d

    source_node = relationship("Node", foreign_keys=[source_node_id], back_populates="demands_as_source")
    dest_node = relationship("Node", foreign_keys=[dest_node_id], back_populates="demands_as_dest")
    flows = relationship("FlowAssignment", foreign_keys="[FlowAssignment.demand_id]", back_populates="demand")


class NetworkParameter(Base):
    __tablename__ = "network_parameters"

    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True)  # U, c_km, c_u
    value = Column(Float)
    description = Column(String)


class ResultLink(Base):
    __tablename__ = "results_links"

    id = Column(Integer, primary_key=True)
    candidate_link_id = Column(Integer, ForeignKey("candidate_links.id"))
    capacity = Column(Float)  # u_e

    candidate_link = relationship("CandidateLink", foreign_keys=[candidate_link_id], back_populates="result_link")


class FlowAssignment(Base):
    __tablename__ = "flow_assignments"

    id = Column(Integer, primary_key=True, index=True)
    demand_id = Column(Integer, ForeignKey("demands.id"), nullable=False)
    link_id = Column(Integer, ForeignKey("candidate_links.id"), nullable=False)
    flow_value = Column(Float, default=0.0) # x_de

    demand = relationship("Demand", foreign_keys=[demand_id], back_populates="flows")
    link = relationship("CandidateLink", foreign_keys=[link_id], back_populates="flows")