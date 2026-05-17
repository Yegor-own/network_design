from typing import List
from v2.core.entities import Link, LinkWithNodes
from v2.core.interfaces import ILinkRepository

class LinkService:
    def __init__(self, link_repo: ILinkRepository):
        self.link_repo = link_repo

    def get_all_links(self) -> List[Link]:
        return self.link_repo.get_all()
    
    def get_all_links_full(self) -> List[LinkWithNodes]:
        return self.link_repo.get_all_full()
    
    def get_link_by_id_full(self, link_id: int) -> Link:
        link = self.link_repo.get_link_by_id_full(link_id)
        if not link:
            raise ValueError(f"Такого пути нет")
        return link

    def create_candidate_link(self, source_id: int, dest_id: int) -> LinkWithNodes:
        if source_id == dest_id:
            raise ValueError("Начальный и конечный узлы не могут совпадать")
        return self.link_repo.create_link(source_id, dest_id)