from fastapi import FastAPI
from v2.src.internal.handlers import node_handler, link_handler, demand_handler, solver_handler, param_handler, result_handler
from v2.src.internal.db.connect import engine, SessionLocal, Base
from v2.src.cmd.db_seed import seed_network_parameters

app = FastAPI()
Base.metadata.create_all(bind=engine)


@app.on_event("startup")
def on_startup():
    db = SessionLocal()
    try:
        seed_network_parameters(db)
    finally:
        db.close()

app.include_router(node_handler.router, prefix="/api/v2", tags=["Nodes"])
app.include_router(link_handler.router, prefix="/api/v2", tags=["Candidate Links"])
app.include_router(demand_handler.router, prefix="/api/v2", tags=["Demands"])
app.include_router(solver_handler.router, prefix="/api/v2", tags=["Solver"])
app.include_router(param_handler.router, prefix="/api/v2", tags=["Parameters"])
app.include_router(result_handler.router, prefix="/api/v2", tags=["Results"])
