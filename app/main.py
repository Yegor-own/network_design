from fastapi import FastAPI
from app.handlers import node_handler, link_handler, demand_handler, solver_handler, param_handler, result_handler
from app.database import engine, Base

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(node_handler.router, prefix="/api/v1", tags=["Nodes"])
app.include_router(link_handler.router, prefix="/api/v1", tags=["Candidate Links"])
app.include_router(demand_handler.router, prefix="/api/v1", tags=["Demands"])
app.include_router(solver_handler.router, prefix="/api/v1", tags=["Solver"])
app.include_router(param_handler.router, prefix="/api/v1", tags=["Parameters"])
app.include_router(result_handler.router, prefix="/api/v1", tags=["Results"])
