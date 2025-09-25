from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("/verifier-sante", summary="Verification de l'etat de l'API")
async def verifier_sante():
    """
    Point de verification simple pour s'assurer que l'API est en cours d'execution.
    """
    return {
        "statut": "OK",
        "message": "API Taxi Tariff Calculator is running",
        "horodatage": datetime.now().isoformat()
    }