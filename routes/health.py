from fastapi import APIRouter
from datetime import datetime
import pytz

router = APIRouter()


@router.get("/verifier-sante", summary="Verification de l'etat de l'API")
async def verifier_sante():
    """
    Point de verification simple pour s'assurer que l'API est en cours d'execution.
    """
    fuseau_france = pytz.timezone('Europe/Paris')
    heure_france = datetime.now(fuseau_france)

    return {
        "statut": "OK",
        "message": "L'API est démarrée",
        "horodatage": heure_france.isoformat()
    }