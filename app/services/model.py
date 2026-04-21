from pyomo.environ import *

def create_model(nodes, links, demands, U_max):

    model = ConcreteModel()

    model.N = Set(initialize=[n.id for n in nodes])
    model.E = Set(initialize=[l.id for l in links])
    model.D = Set(initialize=[d.id for d in demands])

    node_map = {n.id: n for n in nodes}
    link_map = {l.id: l for l in links}
    demand_map = {d.id: d for d in demands}

    edge_from = {l.id: l.source_id for l in links}
    edge_to   = {l.id: l.target_id for l in links}

    model.U = Param(initialize=U_max)

    model.ckm = Param(model.E, initialize={l.id: l.cost_km for l in links})
    model.cu  = Param(model.E, initialize={l.id: l.cost_unit for l in links})
    model.de  = Param(model.E, initialize={l.id: l.distance for l in links})

    model.h = Param(model.D, initialize={d.id: d.volume for d in demands})

    model.z = Var(model.E, domain=Binary)              # активен ли канал
    model.u = Var(model.E, domain=NonNegativeReals)    # capacity
    model.x = Var(model.D, model.E, domain=NonNegativeReals)  # flow

    def objective_rule(m):
        return sum(
            m.ckm[e] * m.de[e] * m.z[e] +
            m.cu[e]  * m.u[e]
            for e in m.E
        )

    model.obj = Objective(rule=objective_rule, sense=minimize)

    def capacity_activation_rule(m, e):
        return m.u[e] <= m.U * m.z[e]

    model.capacity_activation = Constraint(model.E, rule=capacity_activation_rule)

    def capacity_limit_rule(m, e):
        return sum(m.x[d, e] for d in m.D) <= m.u[e]

    model.capacity_limit = Constraint(model.E, rule=capacity_limit_rule)

    def flow_balance_rule(m, d, n):

        inflow = sum(m.x[d, e] for e in m.E if edge_to[e] == n)
        outflow = sum(m.x[d, e] for e in m.E if edge_from[e] == n)

        if n == demand_map[d].source_id:
            return outflow - inflow == m.h[d]
        elif n == demand_map[d].dest_id:
            return outflow - inflow == -m.h[d]
        else:
            return outflow - inflow == 0

    model.flow_balance = Constraint(model.D, model.N, rule=flow_balance_rule)


    return model
