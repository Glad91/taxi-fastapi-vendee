from fastapi import APIRouter
from models.cpam import CourseCPAMRequete, CourseCPAMReponse
from calculators.cpam_calculator import CalculateurTarifsCPAM

router = APIRouter()


@router.post("/calculer-tarif-cpam", summary="Calcul tarif selon convention CPAM 2025", response_model=CourseCPAMReponse)
async def calculer_tarif_cpam(requete: CourseCPAMRequete):
    """
    Calcule le tarif d'une course selon la convention-cadre nationale CPAM 2025.
    Inclut forfaits, majorations, suppléments et abattements transport partagé.
    """
    calculateur_cpam_instance = CalculateurTarifsCPAM(departement=requete.departement)

    resultat = calculateur_cpam_instance.calculer_tarif_cpam(
        distance_km=requete.distance_km,
        ville_depart=requete.ville_depart,
        ville_arrivee=requete.ville_arrivee,
        tarif_nuit=requete.tarif_nuit,
        date_heure_transport=requete.date_heure_transport,
        type_transport=requete.type_transport,
        nb_patients=requete.nb_patients,
        tpmr=requete.tpmr,
        peages=requete.peages
    )

    return resultat