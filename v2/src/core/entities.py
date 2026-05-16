from dataclasses import dataclass
from typing import List

@dataclass
class Node:
    id: int
    name: str
    lat: float
    lng: float

@dataclass
class Link:
    id: int
    source_node_id: int
    dest_node_id: int
    distance: float

@dataclass
class Demand:
    id: int
    source_node_id: int
    dest_node_id: int
    volume: float

@dataclass
class NetworkParameter:
    key: str
    value: float

@dataclass
class ResultLink:
    link_id: int
    capacity: float

@dataclass
class FlowAssignment:
    demand_id: int
    link_id: int
    flow_value: float

@dataclass
class SolverResult:
    links: List[ResultLink]
    flows: List[FlowAssignment]