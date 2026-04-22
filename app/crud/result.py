
from sqlalchemy.orm import Session
from app.models.models import ResultLink, CandidateLink, FlowAssignment

def get_active_links(db: Session):
    results = db.query(
        ResultLink.id,
        ResultLink.candidate_link_id,
        ResultLink.capacity,
        CandidateLink.node_a_id,
        CandidateLink.node_b_id
    ).join(CandidateLink, ResultLink.candidate_link_id == CandidateLink.id).all()
    return results

def get_all_flows(db: Session):
    return db.query(FlowAssignment).all()