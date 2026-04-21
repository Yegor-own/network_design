from sqlalchemy.orm import Session
from app.models.models import Node, CandidateLink, Demand, FlowAssignment  # Не забудь добавить FlowAssignment в модели!
from app.schemas.solver_shema import SolverNode, SolverLink, SolverDemand
from app.services.pyomo_solver import PyomoNetworkSolver
from geoalchemy2.functions import ST_DistanceSphere


def run_network_optimization(db: Session):
    # 1. Вытаскиваем данные из БД
    db_nodes = db.query(Node).all()
    db_links = db.query(CandidateLink).all()
    db_demands = db.query(Demand).all()

    if not db_nodes or not db_links or not db_demands:
        return {"status": "error", "message": "Недостаточно данных для расчета (нужны узлы, линки и требования)"}

    # 2. Мапим данные в DTO для математика
    nodes_dto = []
    for n in db_nodes:
        # Для простоты пока передаем 0,0, так как математик не использует координаты в этой модели
        # Но если понадобятся, ты можешь вытащить их через ST_X/ST_Y
        nodes_dto.append(SolverNode(id=n.id, lat=0.0, lng=0.0))

    links_dto = []
    for l in db_links:
        # ВАЖНО: PDF требует геодезическое расстояние d_e.
        # Давай пока поставим 1.0 или посчитаем просто заглушкой.
        # В идеале тут должен быть запрос к PostGIS для вычисления расстояния.
        links_dto.append(SolverLink(
            id=l.id,
            node_a_id=l.node_a_id,
            node_b_id=l.node_b_id,
            cost_per_km=l.cost_per_km,
            cost_per_unit=l.cost_per_unit,
            distance=1.0  # TODO: Считать реальное расстояние
        ))

    demands_dto = [
        SolverDemand(id=d.id, source_node_id=d.source_node_id, dest_node_id=d.dest_node_id, volume=d.volume)
        for d in db_demands
    ]

    # 3. Запускаем "мозги"
    U_max = 1000.0  # Это значение U из PDF. Его можно вынести в настройки.
    solver = PyomoNetworkSolver()

    try:
        result = solver.solve(nodes_dto, links_dto, demands_dto, U_max)
    except Exception as e:
        return {"status": "error", "message": str(e)}

    # 4. Сохраняем результаты в БД

    # 4.1. Обновляем линки (включен ли и какая емкость)
    for link_id, data in result.links_results.items():
        db_link = db.query(CandidateLink).filter(CandidateLink.id == link_id).first()
        if db_link:
            db_link.is_active = data["z"] > 0.5  # Переводим float в bool
            db_link.capacity = data["u"]

    # 4.2. Обновляем потоки (x_de)
    # Сначала удалим старые результаты маршрутизации
    db.query(FlowAssignment).delete()

    # Записываем новые
    for flow in result.flows:
        new_flow = FlowAssignment(
            demand_id=flow["demand_id"],
            link_id=flow["link_id"],
            flow_value=flow["flow"]
        )
        db.add(new_flow)

    db.commit()

    return {"status": "success", "message": "Расчет успешно завершен"}