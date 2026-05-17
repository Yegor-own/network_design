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
from v2.core.services.node_service import NodeService
from v2.core.services.link_service import LinkService
from v2.core.services.demand_service import DemandService
from v2.core.services.param_service import ParamService

def get_node_service(db: Session = Depends(get_db)) -> NodeService:
    repo = SqlAlchemyNodeRepository(db) 
    return NodeService(repo)

def get_link_service(db: Session = Depends(get_db)) -> LinkService:
    repo = SqlAlchemyLinkRepository(db) 
    return LinkService(repo)

def get_demand_service(db: Session = Depends(get_db)) -> DemandService:
    repo = SqlAlchemyDemandRepository(db) 
    return DemandService(repo)

def get_param_service(db: Session = Depends(get_db)) -> ParamService:
    repo = SqlAlchemyParamRepository(db) 
    return ParamService(repo)

def get_optimization_service(db: Session = Depends(get_db)) ->  OptimizationService:
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