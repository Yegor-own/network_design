from sqlalchemy.orm import Session

from app.crud.demand import get_demands
from app.crud.flow import create_flow
from app.crud.link import get_links_with_distance
from app.crud.node import get_nodes_except_name
from app.crud.result_link import create_result_link
from app.models.models import FlowAssignment, ResultLink
from app.services.solver_interface import SolverNode, SolverLink, SolverDemand
from app.services.pyomo_solver import PyomoNetworkSolver


def run_network_optimization(db: Session):
    db_nodes = get_nodes_except_name(db)
    db_links = get_links_with_distance(db)
    db_demands = get_demands(db)

    if not db_nodes or not db_links or not db_demands:
        return {"status": "error", "message": "Недостаточно данных для расчета"}

    nodes_dto = []
    for node in db_nodes:
        nodes_dto.append(SolverNode.model_validate(node))

    links_dto = []
    for link in db_links:
        links_dto.append(SolverLink.model_validate(link))

    demands_dto = []
    for demand in db_demands:
        demands_dto.append(SolverDemand.model_validate(demand))

    U_max = 1000.0  # TODO from NetParam
    solver = PyomoNetworkSolver()

    try:
        result = solver.solve(nodes_dto, links_dto, demands_dto, U_max)
    except Exception as e:
        return {"status": "error", "message": str(e)}

    for link_id, data in result.links_results.items():
        if data["z"] > 0.5:
            new_rlink = ResultLink(
                candidate_link_id=link_id,
                capacity=data["u"],
            )
            db.add(new_rlink)

    db.query(FlowAssignment).delete()

    for flow in result.flows:
        new_flow = FlowAssignment(
            demand_id=flow["demand_id"],
            link_id=flow["link_id"],
            flow_value=flow["flow"]
        )
        db.add(new_flow)
        # create_flow(db, new_flow)

    db.commit()

    return {"status": "success", "message": "Расчет успешно завершен"}