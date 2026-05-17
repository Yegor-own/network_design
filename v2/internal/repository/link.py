from v2.internal.repository import Session, aliased, List, ST_DistanceSphere, ST_Y, ST_X


from v2.core.entities import Node as NodeEntity, Link, LinkWithNodes
from v2.core.interfaces import ILinkRepository
from v2.internal.models.models import CandidateLink as LinkModel, Node as NodeModel

class SqlAlchemyLinkRepository(ILinkRepository):
    def __init__(self, db: Session):
        self.db = db

    def _row_to_base_entity(self, row) -> Link:
        link_orm, dist = row
        return Link(
            id=link_orm.id,
            source_node_id=link_orm.source_node_id,
            dest_node_id=link_orm.dest_node_id,
            distance=float(dist) if dist else 0.0
        )


    def get_all(self) -> List[Link]:
        Src = aliased(NodeModel)
        Dst = aliased(NodeModel)

        results = self.db.query(
            LinkModel,
            (ST_DistanceSphere(Src.location, Dst.location) / 1000.0).label("distance")
        ).join(Src, LinkModel.source_node_id == Src.id) \
         .join(Dst, LinkModel.dest_node_id == Dst.id).all()
        
        return [self._row_to_base_entity(row) for row in results]

    def get_link_by_id(self, link_id: int) -> Link:
        Src = aliased(NodeModel)
        Dst = aliased(NodeModel)

        result = self.db.query(
            LinkModel,
            (ST_DistanceSphere(Src.location, Dst.location) / 1000.0).label("distance")
        ).join(Src, LinkModel.source_node_id == Src.id) \
         .join(Dst, LinkModel.dest_node_id == Dst.id) \
         .filter(LinkModel.id == link_id).first()
        
        return self._row_to_base_entity(result) if result else None

    def _row_to_full_entity(self, row) -> LinkWithNodes:
        link_orm, dist, s_id, s_name, s_lat, s_lng, d_id, d_name, d_lat, d_lng = row
        
        return LinkWithNodes(
            id=link_orm.id,
            source_node=NodeEntity(id=s_id, name=s_name, lat=s_lat, lng=s_lng),
            dest_node=NodeEntity(id=d_id, name=d_name, lat=d_lat, lng=d_lng),
            distance=float(dist) if dist else 0.0
        )
    
    def get_all_full(self) -> List[LinkWithNodes]:
        Src = aliased(NodeModel)
        Dst = aliased(NodeModel)

        results = self.db.query(
            LinkModel,
            (ST_DistanceSphere(Src.location, Dst.location) / 1000.0).label("distance"),
            Src.id, Src.name, ST_Y(Src.location), ST_X(Src.location), # Данные узла А
            Dst.id, Dst.name, ST_Y(Dst.location), ST_X(Dst.location)  # Данные узла Б
        ).join(Src, LinkModel.source_node_id == Src.id) \
         .join(Dst, LinkModel.dest_node_id == Dst.id).all()
        
        return [self._row_to_full_entity(row) for row in results]

    def create_link(self, source_node_id: int, dest_node_id: int) -> LinkWithNodes:
        new_link = LinkModel(source_node_id=source_node_id, dest_node_id=dest_node_id)
        self.db.add(new_link)
        self.db.commit()
        self.db.refresh(new_link)
        return self.get_link_by_id_full(new_link.id)

    def get_link_by_id_full(self, link_id: int) -> LinkWithNodes:
        Src = aliased(NodeModel)
        Dst = aliased(NodeModel)
        result = self.db.query(
            LinkModel,
            (ST_DistanceSphere(Src.location, Dst.location) / 1000.0).label("distance"),
            Src.id, Src.name, ST_Y(Src.location), ST_X(Src.location),
            Dst.id, Dst.name, ST_Y(Dst.location), ST_X(Dst.location)
        ).join(Src, LinkModel.source_node_id == Src.id) \
         .join(Dst, LinkModel.dest_node_id == Dst.id) \
         .filter(LinkModel.id == link_id).first()
        
        return self._row_to_full_entity(result) if result else None