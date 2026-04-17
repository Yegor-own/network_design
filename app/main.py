from fastapi import FastAPI
from app.api import node_api, candidatelink_api
from app.database import engine, Base

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(node_api.router, prefix="/api/v1", tags=["Nodes"])
app.include_router(candidatelink_api.router, prefix="/api/v1", tags=["Candidate Links"])

@app.get("/")
def health_check():
    return {"status": "alive"}