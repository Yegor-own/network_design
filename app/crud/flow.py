from sqlalchemy.orm import Session
from app.models.models import FlowAssignment

def create_flow(db: Session, flow_in: FlowAssignment):
    db.add(flow_in)
    db.commit()
    db.refresh(flow_in)
    return flow_in