from typing import List
from v2.core.entities import NetworkParameter
from v2.core.interfaces import IParamRepository

class ParamService:
    def __init__(self, param_repo: IParamRepository):
        self.param_repo = param_repo

    def get_all(self) -> List[NetworkParameter]:
        return self.param_repo.get_all()

    def update_parameter(self, key: str, value: float) -> NetworkParameter:
        if value < 0:
            raise ValueError("Значение параметра не может быть отрицательным")
        return self.param_repo.update_parameter(key, value)