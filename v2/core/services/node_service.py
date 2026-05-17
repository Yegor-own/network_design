# v2/core/services/node_service.py
from typing import List
from v2.core.entities import Node
from v2.core.interfaces import INodeRepository

class NodeService:
    def __init__(self, node_repo: INodeRepository):
        self.node_repo = node_repo

    def get_all_nodes(self) -> List[Node]:
        return self.node_repo.get_all()

    def create_node(self, name: str, lat: float, lng: float) -> Node:
        if self.node_repo.get_node_by_name(name):
            raise ValueError(f"Узел с именем '{name}' уже существует")
        return self.node_repo.create_node(name, lat, lng)