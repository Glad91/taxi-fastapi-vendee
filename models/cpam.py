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
    tarif_nuit: bool = Field(False, description="Appliquer tarif nuit/weekend (+50%)")
    date_heure_transport: Optional[datetime] = Field(None, description="Date et heure du transport (optionnel, si tarif_nuit non spécifié)")
    type_transport: TypeTransport = Field(TypeTransport.SIMPLE, description="Type de transport")
    nb_patients: int = Field(1, description="Nombre de patients transportés", ge=1, le=8)
    tpmr: bool = Field(False, description="Transport PMR avec véhicule adapté")
    peages: float = Field(0.0, description="Frais de péage en euros", ge=0)
    departement: str = Field("85", description="Numéro du département")


class DetailsCPAMReponse(BaseModel):
    forfait_prise_charge: float = Field(..., description="Forfait de prise en charge (€)")
    distance_km: float = Field(..., description="Distance totale en kilomètres")
    nb_patients: int = Field(..., description="Nombre de patients transportés")
    forfait_grande_ville: float = Field(..., description="Supplément grande ville (€)")
    km_facturables: float = Field(..., description="Kilomètres facturables (après 4km gratuits)")
    tarif_km: float = Field(..., description="Tarif par kilomètre (€/km)")
    cout_kilometrique: float = Field(..., description="Coût total kilométrique (€)")
    base_tarifaire: float = Field(..., description="Base tarifaire avant majorations (€)")
    majoration_taux: float = Field(..., description="Taux de majoration appliqué (0.0 à 1.0)")
    majoration_type: str = Field(..., description="Type de majoration appliquée")
    majoration_montant: float = Field(..., description="Montant de la majoration (€)")
    supplement_tpmr: float = Field(..., description="Supplément TPMR (€)")
    supplement_drom: float = Field(..., description="Supplément DROM (€)")
    peages: float = Field(..., description="Frais de péage (€)")
    total_supplements: float = Field(..., description="Total des suppléments (€)")
    abattement_partage_taux: float = Field(..., description="Taux d'abattement transport partagé (0.0 à 1.0)")
    abattement_partage_montant: float = Field(..., description="Montant de l'abattement transport partagé (€)")
    departement: str = Field(..., description="Département de facturation")
    date_heure_transport: str = Field(..., description="Date et heure du transport (ISO 8601)")


class CourseCPAMReponse(BaseModel):
    total: float = Field(..., description="Tarif total de la course (€)")
    details: DetailsCPAMReponse = Field(..., description="Détail complet du calcul CPAM")