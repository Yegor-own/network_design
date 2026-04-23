from sqlalchemy.orm import Session
from app.models.models import NetworkParameter


def update_parameter(db: Session, key: str, value: float):
    db_param = db.query(NetworkParameter).filter(NetworkParameter.key == key).first()
    if db_param:
        db_param.value = value
        db.commit()
        db.refresh(db_param)
    return db_param


def get_all_params(db: Session):
    return db.query(NetworkParameter).all()


def get_params_dict(db: Session):
    params = db.query(NetworkParameter).all()
    return {p.key: p.value for p in params}
