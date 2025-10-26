from fastapi import APIRouter
from app.models.schemas import MaintenanceResponse
from app.services.maintenance import clear_all_data

router = APIRouter(tags=["maintenance"])

@router.delete("/maintenance/reset-all", response_model=MaintenanceResponse)
def maintenance_reset_all():
    return clear_all_data()
