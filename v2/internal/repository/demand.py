from v2.internal.repository import Session, aliased, List, ST_Y, ST_X

from v2.core.entities import Node as NodeEntity, Demand, DemandWithNodes
from v2.core.interfaces import IDemandRepository
from v2.internal.models.models import Demand as DemandModel, Node as NodeModel


class SqlAlchemyDemandRepository(IDemandRepository):
    def __init__(self, db: Session):
        self.db = db

    def _row_to_full_entity(self, row) -> DemandWithNodes:
        demand_orm, s_id, s_name, s_lat, s_lng, d_id, d_name, d_lat, d_lng = row
        
        src_node = NodeEntity(id=s_id, name=s_name, lat=s_lat, lng=s_lng)
        dst_node = NodeEntity(id=d_id, name=d_name, lat=d_lat, lng=d_lng)
        
        return DemandWithNodes(
            id=demand_orm.id,
            source_node=src_node,
            dest_node=dst_node,
            volume=demand_orm.volume
        )
    
    def get_all(self) -> List[Demand]:
        results = self.db.query(DemandModel).all()
        return [
            Demand(
                id=d.id,
                source_node_id=d.source_node_id,
                dest_node_id=d.dest_node_id,
                volume=d.volume
            )
            for d in results
        ]

    def get_all_full(self) -> List[DemandWithNodes]:
        Src = aliased(NodeModel)
        Dst = aliased(NodeModel)

        results = self.db.query(
            DemandModel,
            Src.id, Src.name, ST_Y(Src.location), ST_X(Src.location),
            Dst.id, Dst.name, ST_Y(Dst.location), ST_X(Dst.location)
        ).join(Src, DemandModel.source_node_id == Src.id) \
         .join(Dst, DemandModel.dest_node_id == Dst.id) \
         .all()

        return [self._row_to_full_entity(row) for row in results]
    
    def get_demand_by_id_full(self, demand_id: int) -> DemandWithNodes:
        Src = aliased(NodeModel)
        Dst = aliased(NodeModel)

        result = self.db.query(
            DemandModel,
            Src.id, Src.name, ST_Y(Src.location), ST_X(Src.location),
            Dst.id, Dst.name, ST_Y(Dst.location), ST_X(Dst.location)
        ).join(Src, DemandModel.source_node_id == Src.id) \
         .join(Dst, DemandModel.dest_node_id == Dst.id) \
         .filter(DemandModel.id == demand_id).first()
        
        return self._row_to_full_entity(result) if result else None

    def create_demand(self, source_node_id: int, dest_node_id: int, volume: float) -> DemandWithNodes:
        new_demand = DemandModel(
            source_node_id=source_node_id,
            dest_node_id=dest_node_id,
            volume=volume
        )
        self.db.add(new_demand)
        self.db.commit()
        self.db.refresh(new_demand)

        return self.get_demand_by_id_full(new_demand.id)
    
    def delete_demand(self, demand_id: int) -> bool:
        db_demand = self.db.query(DemandModel).filter(DemandModel.id == demand_id).first()
        if not db_demand:
            return False
            
        self.db.delete(db_demand)
        self.db.commit()
        return True
