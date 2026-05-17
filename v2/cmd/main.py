from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from v2.internal.handlers import demand_handler, link_handler, node_handler, param_handler, result_handler
from v2.internal.db.connect import engine, SessionLocal, Base
from v2.cmd.db_seed import seed_network_parameters

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
app.include_router(param_handler.router, prefix="/api/v2", tags=["Parameters"])
app.include_router(result_handler.router, prefix="/api/v2", tags=["Results"])
