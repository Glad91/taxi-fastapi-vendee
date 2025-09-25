from fastapi import APIRouter, HTTPException, Body, Query
from models.taxi import CourseRequete, CourseReponse, EstimationRapideReponse
from calculators.taxi_calculator import CalculateurTarifsTaxi

router = APIRouter()
calculateur = CalculateurTarifsTaxi()


@router.post("/calculer-tarif", summary="Calcul du tarif detaille d'une course", response_model=CourseReponse)
async def calculer_tarif_course(course_requete: CourseRequete = Body(...)):
    """
    Calcule le tarif total d'une course de taxi en fonction de la distance, du temps d'attente, de l'heure de depart et du type de trajet.
    """
    if course_requete.distance_km < 0:
        raise HTTPException(status_code=400, detail="La distance ne peut pas etre negative.")

    resultat = calculateur.calculer_tarif_course(
        distance_km=course_requete.distance_km,
        minutes_attente=course_requete.minutes_attente,
        date_heure_depart=course_requete.date_heure_depart,
        aller_retour=course_requete.aller_retour
    )
    return resultat


@router.get("/tarifs", summary="Recuperation des tarifs actuels")
async def recuperer_tarifs_actuels():
    """
    Retourne les tarifs officiels actuels utilises pour les calculs.
    """
    return {
        "prix_base": calculateur.prix_base,
        "tarif_a_aller_retour_jour": calculateur.tarif_a_jour,
        "tarif_b_aller_retour_nuit": calculateur.tarif_b_nuit,
        "tarif_c_simple_jour": calculateur.tarif_c_jour,
        "tarif_d_simple_nuit": calculateur.tarif_d_nuit,
        "prix_par_minute_attente": calculateur.prix_par_minute_attente,
        "heures_de_nuit": f"{calculateur.debut_nuit} - {calculateur.fin_nuit}",
        "tarif_minimum": calculateur.tarif_minimum
    }


@router.get("/estimation-rapide", summary="Estimation rapide via parametres GET", response_model=EstimationRapideReponse)
async def estimation_rapide(
    distance_km: float = Query(..., description="Distance de la course en kilometres.", gt=0),
    minutes_attente: float = Query(0, description="Temps d'attente en minutes.", ge=0),
    aller_retour: bool = Query(False, description="Indique s'il s'agit d'un aller-retour.")
):
    """
    Fournit une estimation rapide du tarif d'une course.
    """
    resultat = calculateur.calculer_tarif_course(
        distance_km=distance_km,
        minutes_attente=minutes_attente,
        aller_retour=aller_retour
    )

    return {
        "distance_km": distance_km,
        "aller_retour": aller_retour,
        "total_estime": resultat["total"],
        "type_tarif": resultat["type_tarif"]
    }