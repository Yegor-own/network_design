from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from v1.database import get_db
from v1.services.optimization_service import run_network_optimization

router = APIRouter()

@router.post("/calculate", summary="Запустить расчет оптимальной топологии")
def calculate_topology(db: Session = Depends(get_db)):
    result = run_network_optimization(db)

    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])

    return result