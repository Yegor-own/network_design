from v2.internal.repository import Session, List

from v2.core.entities import NetworkParameter as ParameterEntity
from v2.core.interfaces import IParamRepository
from v2.internal.models.models import NetworkParameter as ParameterModel

class SqlAlchemyParamRepository(IParamRepository):
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self) -> List[ParameterEntity]:
        results = self.db.query(ParameterModel).all()
        return [
            ParameterEntity(
                id=p.id,
                key=p.key,
                value=p.value,
                description=p.description
            ) for p in results
        ]

    def update_parameter(self, key: str, value: float) -> ParameterEntity:
        db_param = self.db.query(ParameterModel).filter(ParameterModel.key == key).first()
        
        if not db_param:
            return None

        db_param.value = value
        self.db.commit()
        self.db.refresh(db_param)

        return ParameterEntity(
            id=db_param.id,
            key=db_param.key,
            value=db_param.value,
            description=db_param.description
        )

