from fastapi import FastAPI
from v1.handlers import node_handler, link_handler, demand_handler, solver_handler, param_handler, result_handler
from v1.database import engine, SessionLocal, Base
from v1.db_seed import seed_network_parameters

app = FastAPI()
Base.metadata.create_all(bind=engine)


@app.on_event("startup")
def on_startup():
    db = SessionLocal()
    try:
        seed_network_parameters(db)
    finally:
        db.close()

app.include_router(node_handler.router, prefix="/api/v1", tags=["Nodes"])
app.include_router(link_handler.router, prefix="/api/v1", tags=["Candidate Links"])
app.include_router(demand_handler.router, prefix="/api/v1", tags=["Demands"])
app.include_router(solver_handler.router, prefix="/api/v1", tags=["Solver"])
app.include_router(param_handler.router, prefix="/api/v1", tags=["Parameters"])
app.include_router(result_handler.router, prefix="/api/v1", tags=["Results"])
