
from repository import Session

from v2.core.interfaces import IResultRepository
from v2.core.entities import SolverResult
from v2.internal.models.models import ResultLink, CandidateLink, FlowAssignment

class SqlAlchemyResultRepository(IResultRepository):
    def __init__(self, db: Session):
        self.db = db

    def clear_previous_results(self) -> None:
        self.db.query(FlowAssignment).delete()
        self.db.query(ResultLink).delete()
        self.db.commit()

    def save_optimization_result(self, result: SolverResult) -> None:
        for r_link in result.links:
            new_rlink = ResultLink(
                candidate_link_id=r_link.link_id,
                capacity=r_link.capacity,
            )
            self.db.add(new_rlink)
            
        for flow in result.flows:
            new_flow = FlowAssignment(
                demand_id=flow.demand_id,
                link_id=flow.link_id,
                flow_value=flow.flow_value
            )
            self.db.add(new_flow)

        self.db.commit()

    def get_active_links(self):
        results = self.db.query(
            ResultLink.id,
            ResultLink.candidate_link_id,
            ResultLink.capacity,
            CandidateLink.node_a_id,
            CandidateLink.node_b_id
        ).join(CandidateLink, ResultLink.candidate_link_id == CandidateLink.id).all()
        return results

    def get_all_flows(self):
        return self.db.query(FlowAssignment).all()