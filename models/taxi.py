from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class CourseRequete(BaseModel):
    """
    Details de la course pour le calcul du tarif.
    """
    distance_km: float = Field(..., description="Distance de la course en kilometres.")
    minutes_attente: float = Field(0, description="Temps d'attente en minutes.", ge=0)
    date_heure_depart: Optional[datetime] = Field(None, description="Date et heure de depart (ISO 8601).")
    aller_retour: bool = Field(False, description="Indique s'il s'agit d'un aller-retour.")


class CourseReponse(BaseModel):
    """
    Resultat detaille du calcul de la course.
    """
    prix_base: float
    distance_km: float
    distance_facturable: float
    cout_distance: float
    minutes_attente: float
    cout_attente: float
    type_tarif: str
    aller_retour: bool
    tarif_km: float
    tarif_minimum_applique: bool
    total: float
    date_heure_depart: str


class EstimationRapideReponse(BaseModel):
    """
    Resultat d'une estimation rapide.
    """
    distance_km: float
    aller_retour: bool
    total_estime: float
    type_tarif: str