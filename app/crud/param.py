from sqlalchemy.orm import Session
from app.models.models import NetworkParameter


def update_param_by_key(db: Session, key: str, value: float):
    # 1. Ищем запись по уникальному ключу
    db_param = db.query(NetworkParameter).filter(NetworkParameter.key == key).first()

    if db_param:
        # 2. Обновляем значение
        db_param.value = value
        db.commit()
        db.refresh(db_param)
    return db_param


def get_all_params(db: Session):
    return db.query(NetworkParameter).all()