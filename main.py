from fastapi import FastAPI, HTTPException, Body, Query
from pydantic import BaseModel, Field
from datetime import datetime, time, date, timezone, timedelta
from typing import Optional
from enum import Enum
import pytz

# --- Classe de Calculateur de Tarifs ---

class TypeTransport(str, Enum):
    SIMPLE = "simple"
    HOSPITALISATION = "hospitalisation"

class CalculateurTarifsTaxi:
    """
    Calcule les tarifs de taxi selon la reglementation Vendee 2025.
    """
    def __init__(self):
        # Tarifs officiels Vendee 2025
        self.prix_base = 2.94  # Prise en charge
        # Tarifs aller simple (de base)
        self.tarif_c_jour = 2.16  # €/km aller simple jour (Tarif C)
        self.tarif_d_nuit = 3.24  # €/km aller simple nuit/dimanche/feries (Tarif D)
        # Tarifs aller-retour
        self.tarif_a_jour = 1.08  # €/km aller-retour jour (Tarif A)
        self.tarif_b_nuit = 1.62  # €/km aller-retour nuit/dimanche/feries (Tarif B)
        self.prix_par_minute_attente = 29.44 / 60  # €/minute d'attente (29,44€/heure)
        self.debut_nuit = time(19, 0)  # 19h00
        self.fin_nuit = time(7, 0)  # 7h00
        self.tarif_minimum = 8.0  # Tarif minimum
        # Fuseau horaire français avec gestion automatique été/hiver
        self.fuseau_france = pytz.timezone('Europe/Paris')

    def est_tarif_nuit(self, date_heure_depart: time) -> bool:
        """Determine si c'est un tarif de nuit (19h-7h) ou dimanche/ferie"""
        return date_heure_depart >= self.debut_nuit or date_heure_depart <= self.fin_nuit

    def est_dimanche(self, date_depart: date) -> bool:
        """Verifie si c'est dimanche"""
        return date_depart.weekday() == 6  # 6 = dimanche

    def obtenir_heure_france(self) -> datetime:
        """Retourne l'heure actuelle en France avec gestion automatique été/hiver"""
        return datetime.now(self.fuseau_france)

    def calculer_tarif_course(self, distance_km: float, minutes_attente: float = 0, date_heure_depart: Optional[datetime] = None, aller_retour: bool = False):
        """Calcule le tarif total de la course"""
        if date_heure_depart is None:
            date_heure_depart = self.obtenir_heure_france()
        # Si une heure est fournie sans timezone, on assume qu'elle est en heure française
        elif date_heure_depart.tzinfo is None:
            date_heure_depart = self.fuseau_france.localize(date_heure_depart)

        total = self.prix_base
        est_nuit_ou_dimanche = self.est_dimanche(date_heure_depart.date()) or self.est_tarif_nuit(date_heure_depart.time())

        if aller_retour:
            if est_nuit_ou_dimanche:
                tarif_km = self.tarif_b_nuit
                type_tarif = "dimanche/ferie aller-retour (tarif B)" if self.est_dimanche(date_heure_depart.date()) else "nuit aller-retour (tarif B)"
            else:
                tarif_km = self.tarif_a_jour
                type_tarif = "jour aller-retour (tarif A)"
        else:
            if est_nuit_ou_dimanche:
                tarif_km = self.tarif_d_nuit
                type_tarif = "dimanche/ferie aller simple (tarif D)" if self.est_dimanche(date_heure_depart.date()) else "nuit aller simple (tarif D)"
            else:
                tarif_km = self.tarif_c_jour
                type_tarif = "jour aller simple (tarif C)"

        # Calcul de la distance facturable
        distance_facturable = distance_km * 2 if aller_retour else distance_km
        cout_distance = distance_facturable * tarif_km
        total += cout_distance

        cout_attente = minutes_attente * self.prix_par_minute_attente
        total += cout_attente

        total_avant_minimum = total
        if total < self.tarif_minimum:
            total = self.tarif_minimum

        return {
            "prix_base": round(self.prix_base, 2),
            "distance_km": distance_km,
            "distance_facturable": round(distance_facturable, 2),
            "cout_distance": round(cout_distance, 2),
            "minutes_attente": minutes_attente,
            "cout_attente": round(cout_attente, 2),
            "type_tarif": type_tarif,
            "aller_retour": aller_retour,
            "tarif_km": round(tarif_km, 2),
            "tarif_minimum_applique": total == self.tarif_minimum,
            "total": round(total, 2),
            "date_heure_depart": date_heure_depart.isoformat()
        }

class CalculateurTarifsCPAM:
    def __init__(self, departement: str = "85"):
        self.departement = departement
        self.forfait_prise_charge = 13.0
        self.forfait_grande_ville = 15.0

        self.villes_grande_ville = [
            "marseille", "paris", "nice", "toulouse", "lyon", "strasbourg",
            "montpellier", "rennes", "bordeaux", "lille", "grenoble", "nantes"
        ]
        self.departements_grande_ville = ["92", "93", "94"]

        self.tarifs_km = {
            "85": 1.07
        }

        self.supplement_tpmr = 30.0
        self.supplement_drom = 3.0
        self.departements_drom = ["971", "972", "973", "974", "976"]

        self.majoration_nuit_weekend = 0.5
        self.majoration_hospitalisation_courte = 0.25
        self.majoration_hospitalisation_longue = 0.50

        self.abattements_partage = {
            2: 0.23,
            3: 0.35,
            4: 0.37
        }

        self.debut_nuit = time(20, 0)
        self.fin_nuit = time(8, 0)

    def est_tarif_nuit(self, heure: time) -> bool:
        return heure >= self.debut_nuit or heure <= self.fin_nuit

    @staticmethod
    def est_weekend_ou_ferie(date_transport: date) -> bool:
        jour_semaine = date_transport.weekday()
        return jour_semaine == 6

    def calculer_tarif_cpam(self,
                           distance_km: float,
                           ville_depart: str = "",
                           ville_arrivee: str = "",
                           date_heure_transport: Optional[datetime] = None,
                           type_transport: TypeTransport = TypeTransport.SIMPLE,
                           nb_patients: int = 1,
                           tpmr: bool = False,
                           peages: float = 0.0):
        if date_heure_transport is None:
            date_heure_transport = datetime.now(pytz.timezone('Europe/Paris'))
        elif date_heure_transport.tzinfo is None:
            date_heure_transport = pytz.timezone('Europe/Paris').localize(date_heure_transport)

        total = self.forfait_prise_charge
        details = {
            "forfait_prise_charge": self.forfait_prise_charge,
            "distance_km": distance_km,
            "nb_patients": nb_patients
        }

        forfait_gv = 0.0
        if (ville_depart.lower() in self.villes_grande_ville or
            ville_arrivee.lower() in self.villes_grande_ville or
            self.departement in self.departements_grande_ville):
            forfait_gv = self.forfait_grande_ville
            total += forfait_gv

        km_facturables = max(0.0, distance_km - 4)
        tarif_km = self.tarifs_km.get(self.departement, 1.07)
        cout_km = km_facturables * tarif_km
        total += cout_km

        base_tarifaire = total

        majoration_appliquee = 0.0
        type_majoration = ""

        if (self.est_tarif_nuit(date_heure_transport.time()) or
            CalculateurTarifsCPAM.est_weekend_ou_ferie(date_heure_transport.date())):
            majoration_appliquee = self.majoration_nuit_weekend
            type_majoration = "nuit/weekend"

        if type_transport == TypeTransport.HOSPITALISATION:
            if distance_km < 50:
                maj_hosp = self.majoration_hospitalisation_courte
            else:
                maj_hosp = self.majoration_hospitalisation_longue

            if maj_hosp > majoration_appliquee:
                majoration_appliquee = maj_hosp
                type_majoration = f"hospitalisation ({'<50km' if distance_km < 50 else '>=50km'})"

        montant_majoration = base_tarifaire * majoration_appliquee
        total += montant_majoration

        supplements = 0.0

        if tpmr:
            supplements += self.supplement_tpmr

        if self.departement in self.departements_drom:
            supplements += self.supplement_drom

        supplements += peages

        # Pour transport partagé : multiplier le tarif total par le nombre de patients
        abattement_taux = 0.0
        abattement_montant = 0.0

        if nb_patients > 1:
            # Multiplier le tarif (base + majoration) par le nombre de patients
            total_avant_supplements = total * nb_patients
            # Ajouter les suppléments
            total = total_avant_supplements + supplements

            # Appliquer l'abattement sur le total (hors suppléments TPMR et péages)
            base_abattement = total - supplements + (self.supplement_tpmr if tpmr else 0)
            abattement_taux = self.abattements_partage.get(min(nb_patients, 4), self.abattements_partage[4])
            abattement_montant = base_abattement * abattement_taux
            total -= abattement_montant
        else:
            # Patient unique : logique normale
            total += supplements

        return {
            "total": round(total, 2),
            "details": {
                **details,
                "forfait_prise_charge": self.forfait_prise_charge,
                "forfait_grande_ville": forfait_gv,
                "km_facturables": round(km_facturables, 2),
                "tarif_km": tarif_km,
                "cout_kilometrique": round(cout_km, 2),
                "base_tarifaire": round(base_tarifaire, 2),
                "majoration_taux": majoration_appliquee,
                "majoration_type": type_majoration,
                "majoration_montant": round(montant_majoration, 2),
                "supplement_tpmr": self.supplement_tpmr if tpmr else 0.0,
                "supplement_drom": self.supplement_drom if self.departement in self.departements_drom else 0.0,
                "peages": peages,
                "total_supplements": round(supplements, 2),
                "abattement_partage_taux": abattement_taux,
                "abattement_partage_montant": round(abattement_montant, 2),
                "departement": self.departement,
                "date_heure_transport": date_heure_transport.isoformat()
            }
        }

# --- Modeles de donnees Pydantic ---

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

# --- Initialisation de l'API ---

app = FastAPI(
    title="API Taxi Vendee 2025",
    description="Une API pour calculer les tarifs de taxi en Vendee, basee sur les tarifs officiels de 2025. La documentation est generee automatiquement par FastAPI.",
    version="1.0.0",
)

# Instance du calculateur
calculateur = CalculateurTarifsTaxi()

# Instance du calculateur CPAM
calculateur_cpam = CalculateurTarifsCPAM()

# --- Endpoints de l'API ---

@app.get("/verifier-sante", summary="Verification de l'etat de l'API")
async def verifier_sante():
    """
    Point de verification simple pour s'assurer que l'API est en cours d'execution.
    """
    return {
        "statut": "OK",
        "message": "API Taxi Tariff Calculator is running",
        "horodatage": datetime.now().isoformat()
    }

@app.post("/calculer-tarif", summary="Calcul du tarif detaille d'une course", response_model=CourseReponse)
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

@app.get("/tarifs", summary="Recuperation des tarifs actuels")
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

@app.get("/estimation-rapide", summary="Estimation rapide via parametres GET", response_model=EstimationRapideReponse)
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

@app.post("/calculer-tarif-cpam", summary="Calcul tarif selon convention CPAM 2025", response_model=CourseCPAMReponse)
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
        date_heure_transport=requete.date_heure_transport,
        type_transport=requete.type_transport,
        nb_patients=requete.nb_patients,
        tpmr=requete.tpmr,
        peages=requete.peages
    )

    return resultat


# Pour lancer l'application en ligne de commande :
# uvicorn api:app --reload
