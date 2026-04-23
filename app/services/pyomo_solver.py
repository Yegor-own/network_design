from pyomo.environ import SolverFactory
from app.services.solver_interface import INetworkSolver, SolverResult
from app.services.model import create_model


class PyomoNetworkSolver(INetworkSolver):

    def solve(self, nodes, links, demands, U_max, cost_km, cost_u):

        model = create_model(nodes, links, demands, U_max, cost_km,cost_u)

        solver = SolverFactory("cbc")
        result = solver.solve(model)

        status = result.solver.termination_condition

        if str(status) != "optimal":
            raise Exception(f"Solver failed: {status}")

        links_results = {}

        for e in model.E:
            links_results[e] = {
                "z": float(model.z[e].value),
                "u": float(model.u[e].value)
            }

        flows = []

        for d in model.D:
            for e in model.E:
                val = model.x[d, e].value

                if val is not None and val > 1e-6:
                    flows.append({
                        "demand_id": int(d),
                        "link_id": int(e),
                        "flow": float(val)
                    })

        return SolverResult(
            links_results=links_results,
            flows=flows
        )
