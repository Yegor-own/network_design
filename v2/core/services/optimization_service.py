from v2.core.interfaces import (
    INodeRepository, ILinkRepository, IDemandRepository, 
    IParamRepository, IResultRepository, INetworkSolver
)

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
        links = self.link_repo.get_all_with_distance()
        demands = self.demand_repo.get_all()
        
        params_list = self.param_repo.get_params_dict() 
        params_dict = {p.key: p.value for p in params_list}

        if not nodes or not links or not demands:
            raise ValueError("Недостаточно данных для расчета")

        result = self.solver.solve(nodes, links, demands, params_dict)

        self.result_repo.clear_previous_results()
        self.result_repo.save_optimization_result(result)

        return {"status": "success", "message": "Расчет успешно завершен"}