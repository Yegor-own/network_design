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
class LinkWithNodes:
    id: int
    source_node: Node
    dest_node: Node
    distance: float

@dataclass
class Demand:
    id: int
    source_node_id: int
    dest_node_id: int
    volume: float

@dataclass
class DemandWithNodes:
    id: int
    source_node: Node
    dest_node: Node
    volume: float

@dataclass
class NetworkParameter:
    id: int
    key: str
    value: float
    description: str

@dataclass
class ResultLink:
    id: int
    link_id: int
    capacity: float

@dataclass
class FlowAssignment:
    id: int
    demand_id: int
    link_id: int
    flow_value: float

@dataclass
class SolverResult:
    links: List[ResultLink]
    flows: List[FlowAssignment]

@dataclass
class NetworkCost:
    total_cost: float
    links_fixed_cost: float
    capacity_cost: float

@dataclass
class OptimizationResponse:
    status: str
    message: str
    total_cost: float
    links_built_count: int 
    flows_assigned_count: int