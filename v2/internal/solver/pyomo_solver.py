from pyomo.environ import SolverFactory
from v2.internal.solver.model import create_model
from v2.core.interfaces import INetworkSolver
from v2.core.entities import (
    SolverResult,
    ResultLink,
    FlowAssignment
)


class PyomoNetworkSolver(INetworkSolver):

    def solve(self, nodes, links, demands, params):

        model = create_model(nodes, links, demands, params)

        solver = SolverFactory("cbc")
        result = solver.solve(model)

        status = result.solver.termination_condition

        if str(status) != "optimal":
            raise Exception(f"Solver failed: {status}")

        links_results = []

        for e in model.E:
            z_val = model.z[e].value or 0.0
            u_val = model.u[e].value or 0.0
            if z_val > 0.5:
                links_results.append(
                    ResultLink(
                        id=0,
                        link_id=int(e),
                        capacity=float(u_val)
                    ))
        flows = []

        for d in model.D:
            for e in model.E:
                val = model.x[d, e].value

                if val is not None and val > 1e-6:
                    flows.append( FlowAssignment(
                        id=0,
                        demand_id=int(d),
                        link_id=int(e),
                        flow_value=float(val)
                    ))

        return SolverResult(
            links=links_results,
            flows=flows
        )