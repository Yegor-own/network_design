from v2.core.interfaces import (
    INodeRepository, ILinkRepository, IDemandRepository, 
    IParamRepository, IResultRepository, INetworkSolver
)
from v2.core.entities import SolverResult, ResultLink, FlowAssignment, OptimizationResponse
from typing import List

class OptimizationService:
    def __init__(
        self,
        node_repo: INodeRepository,
        link_repo: ILinkRepository,
        demand_repo: IDemandRepository,
        param_repo: IParamRepository,
        result_repo: IResultRepository,
        solver: INetworkSolver
    ):
        self.node_repo = node_repo
        self.link_repo = link_repo
        self.demand_repo = demand_repo
        self.param_repo = param_repo
        self.result_repo = result_repo
        self.solver = solver

    def run_optimization(self):
        nodes = self.node_repo.get_all()
        links = self.link_repo.get_all()
        demands = self.demand_repo.get_all()
        
        params = self.param_repo.get_all() 
        # params_dict = {p.key: p.value for p in params_list}

        if not nodes or not links or not demands:
            raise ValueError("Недостаточно данных для расчета")

        result = self.solver.solve(nodes, links, demands, params)

        self.result_repo.clear_previous_results()
        self.result_repo.save_optimization_result(result)

        cost_info = self.get_total_cost()

        return OptimizationResponse(
            status="success",
            message="Расчет успешно завершен",
            total_cost=cost_info.total_cost,
            links_built_count=len(result.links),
            flows_assigned_count=len(result.flows)
        )
    
    def get_results(self) -> SolverResult:
        return {
            "links": self.result_repo.get_result_links(),
            "flows": self.result_repo.get_flows()
        }
    
    def get_result_links(self) -> List[ResultLink]:
        return self.result_repo.get_result_links()
    
    def get_flows(self) -> List[FlowAssignment]:
        return self.result_repo.get_flows()
    
    def get_total_cost(self) -> NetworkCost:
        params = {p.key: p.value for p in self.param_repo.get_all()}
        c_km = params.get("c_km", 0.0)
        c_u = params.get("c_u", 0.0)
        
        return self.result_repo.calculate_total_cost(c_km, c_u)