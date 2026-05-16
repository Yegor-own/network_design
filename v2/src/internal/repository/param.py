from sqlalchemy.orm import Session
from typing import List

from v2.src.core.entities import NetworkParameter
from v2.src.core.interfaces import IParamRepository
from v2.src.internal.models.models import NetworkParameter as NetworkParameterModel

class SqlAlchemyParamRepository(IParamRepository):
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self) -> List[NetworkParameter]:
        results = self.db.query(NetworkParameterModel).all()

        params: List[NetworkParameter] = []
        for param in results:
            params.append(NetworkParameter(
                id=param.id,
                key=param.key,
                value=param.value,
                description=param.description
            ))
        return params

    def update_parameter(self, key: str, value: float) -> NetworkParameter:
        param = self.db.query(NetworkParameterModel).filter(NetworkParameterModel.key == key).first()
        if param:
            param.value = value
            self.db.commit()
            self.db.refresh(param)

        return NetworkParameter(
                key=param.key,
                value=param.value
            )

