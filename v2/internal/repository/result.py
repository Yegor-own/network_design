
from v2.internal.repository import Session, List

from v2.core.interfaces import IResultRepository
from v2.core.entities import SolverResult
from v2.internal.models.models import ResultLink as ResultLinkModel, FlowAssignment as FlowAssignmentModel
from v2.core.entities import ResultLink as ResultLinkEntity, FlowAssignment as FlowAssignmentEntity

class SqlAlchemyResultRepository(IResultRepository):
    def __init__(self, db: Session):
        self.db = db

    def clear_previous_results(self) -> None:
        self.db.query(FlowAssignmentModel).delete()
        self.db.query(ResultLinkModel).delete()
        self.db.commit()

    def save_optimization_result(self, result: SolverResult) -> None:
        for r_link in result.links:
            new_rlink = ResultLinkModel(
                candidate_link_id=r_link.link_id,
                capacity=r_link.capacity,
            )
            self.db.add(new_rlink)
            
        for flow in result.flows:
            new_flow = FlowAssignmentModel(
                demand_id=flow.demand_id,
                link_id=flow.link_id,
                flow_value=flow.flow_value
            )
            self.db.add(new_flow)

        self.db.commit()

    def get_result_links(self) -> List[ResultLinkEntity]:
        results = self.db.query(ResultLinkModel).all()
        return [
            ResultLinkEntity(id=l.id, link_id=l.candidate_link_id, capacity=l.capacity)
            for l in results
        ]

    def get_flows(self) -> List[FlowAssignmentEntity]:
        results = self.db.query(FlowAssignmentModel).all()
        return [
            FlowAssignmentEntity(id=f.id, demand_id=f.demand_id, link_id=f.link_id, flow_value=f.flow_value)
            for f in results
        ]