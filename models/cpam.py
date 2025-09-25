from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum


class TypeTransport(str, Enum):
    SIMPLE = "simple"
    HOSPITALISATION = "hospitalisation"


class CourseCPAMRequete(BaseModel):
    distance_km: float = Field(..., description="Distance en kilomètres", gt=0)
    ville_depart: str = Field("", description="Ville de départ")
    ville_arrivee: str = Field("", description="Ville d'arrivée")
    date_heure_transport: Optional[datetime] = Field(None, description="Date et heure du transport")
    type_transport: TypeTransport = Field(TypeTransport.SIMPLE, description="Type de transport")
    nb_patients: int = Field(1, description="Nombre de patients transportés", ge=1, le=8)
    tpmr: bool = Field(False, description="Transport PMR avec véhicule adapté")
    peages: float = Field(0.0, description="Frais de péage en euros", ge=0)
    departement: str = Field("85", description="Numéro du département")


class CourseCPAMReponse(BaseModel):
    total: float
    details: dict