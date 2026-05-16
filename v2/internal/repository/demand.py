from repository import Session, aliased, List

from v2.core.entities import Node, DemandWithNodes
from v2.core.interfaces import IDemandRepository
from v2.internal.models.models import Demand as DemandModel, Node as NodeModel


class SqlAlchemyDemandRepository(IDemandRepository):
    def __init__(self, db: Session):
        self.db = db

    def sql_to_demand(row) -> DemandWithNodes:
        demand, src, dst = row
        src_node = Node(
            id=src.id,
            name=src.name,
            lat=src.lat,
            lng=src.lng
        )
        dst_node = Node(
            id=dst.id,
            name=dst.name,
            lat=dst.lat,
            lng=dst.lng
        )
        return DemandWithNodes(
            id=demand.id,
            source_node=src_node,
            dest_node=dst_node,
            volume=demand.volume
        )

    def get_all(self) -> List[DemandWithNodes]:
        Source = aliased(NodeModel)
        Dest = aliased(NodeModel)

        results = self.db.query(
            DemandModel,
            Source,
            Dest
        ).join(Source, DemandModel.source_node_id == Source.id) \
            .join(Dest, DemandModel.dest_node_id == Dest.id) \
            .all()

        demands: List[DemandWithNodes] = []
        for row in results:
            demand = self.sql_to_demand(row)
            demands.append(demand)
        return demands
    
    def get_demand_by_id(self, demand_id: int) -> DemandWithNodes:
        Source = aliased(NodeModel)
        Dest = aliased(NodeModel)

        result = self.db.query(
            DemandModel,
            Source,
            Dest
        ).join(Source, DemandModel.source_node_id == Source.id) \
            .join(Dest, DemandModel.dest_node_id == Dest.id) \
            .filter(DemandModel.id == demand_id).first()
        
        if result:
            return self.sql_to_linkwithnodes(result)
        return None
    
    def create_demand(self, source_node_id, dest_node_id, volume) -> DemandWithNodes:
        new_demand = DemandModel(
            source_node_id=source_node_id,
            dest_node_id=dest_node_id,
            volume=volume
        )
        self.db.add(new_demand)
        self.db.commit()
        self.db.refresh(new_demand)

        Source = aliased(NodeModel)
        Dest = aliased(NodeModel)

        result = self.db.query(
            DemandModel,
            Source,
            Dest
        ).join(Source, DemandModel.source_node_id == Source.id) \
            .join(Dest, DemandModel.dest_node_id == Dest.id) \
            .filter(DemandModel.id == new_demand.id).first()
        return self.sql_to_demand(result)
    
    def delete_demand(self, demand_id) -> bool:
        db_demand = self.db.query(DemandModel).filter(DemandModel.id == demand_id).first()
        
        if not db_demand:
            return False
            
        self.db.delete(db_demand)
        self.db.commit()
        return True
