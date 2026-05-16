from sqlalchemy.orm import Session
from typing import List

from v2.src.core.entities import NetworkParameter
from v2.src.core.interfaces import IParamRepository
from v2.src.internal.models import NetworkParameter as NetworkParameterModel

class SqlAlchemyParamRepository(IParamRepository):
    def __init__(self, db: Session):
        self.db = db
    
    def get_params_dict(self) -> List[NetworkParameter]:
        params = self.db.query(NetworkParameterModel).all()
        return {p.key: p.value for p in params}

    def update_parameter(self, key: str, value: float) -> NetworkParameter:
        db_param = self.db.query(NetworkParameterModel).filter(NetworkParameterModel.key == key).first()
        if db_param:
            db_param.value = value
            self.db.commit()
            self.db.refresh(db_param)
        return db_param

