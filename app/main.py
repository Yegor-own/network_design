from fastapi import FastAPI
from app.api import node_api

app = FastAPI()

# "Приклеиваем" роуты из других файлов
app.include_router(node_api.router, prefix="/api/v1", tags=["Nodes"])

@app.get("/")
def health_check():
    return {"status": "alive"}