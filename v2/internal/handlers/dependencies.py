from sqlalchemy.orm import Session
from fastapi import Depends

from v2.internal.db.connect import get_db
from v2.internal.repository.node import SqlAlchemyNodeRepository
from v2.internal.repository.link import SqlAlchemyLinkRepository
from v2.internal.repository.demand import SqlAlchemyDemandRepository
from v2.internal.repository.param import SqlAlchemyParamRepository
from v2.internal.repository.result import SqlAlchemyResultRepository
from v2.internal.solver.pyomo_solver import PyomoNetworkSolver
from v2.core.services.optimization_service import OptimizationService

def get_optimization_service(db: Session = Depends(get_db)):
    node_repo = SqlAlchemyNodeRepository(db)
    link_repo = SqlAlchemyLinkRepository(db)
    demand_repo = SqlAlchemyDemandRepository(db)
    param_repo = SqlAlchemyParamRepository(db)
    result_repo = SqlAlchemyResultRepository(db)
    
    solver = PyomoNetworkSolver() 

    return OptimizationService(
        node_repo, link_repo, demand_repo, 
        param_repo, result_repo, solver
    )