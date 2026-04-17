from fastapi import FastAPI
from app.handlers import node_handler, link_handler
from app.database import engine, Base

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(node_handler.router, prefix="/handlers/v1", tags=["Nodes"])
app.include_router(link_handler.router, prefix="/handlers/v1", tags=["Candidate Links"])

@app.get("/")
def health_check():
    return {"status": "alive"}