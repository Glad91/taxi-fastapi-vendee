from datetime import datetime, time, date
from typing import Optional
from functools import lru_cache
import pytz
from models.cpam import TypeTransport


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

    @lru_cache(maxsize=500)
    def _calculer_base_cpam(self, distance_km: float, ville_depart: str, ville_arrivee: str,
                           tarif_nuit: bool, type_transport: str, nb_patients: int,
                           tpmr: bool, peages: float):
        """Calcul de base CPAM avec cache (paramètres hashables uniquement)"""
        total = self.forfait_prise_charge

        # Forfait grande ville
        forfait_gv = 0.0
        if (ville_depart.lower() in self.villes_grande_ville or
            ville_arrivee.lower() in self.villes_grande_ville or
            self.departement in self.departements_grande_ville):
            forfait_gv = self.forfait_grande_ville
            total += forfait_gv

        # Calcul kilométrique
        km_facturables = max(0.0, distance_km - 4)
        tarif_km = self.tarifs_km.get(self.departement, 1.07)
        cout_km = km_facturables * tarif_km
        total += cout_km

        base_tarifaire = total

        # Majorations
        majoration_appliquee = 0.0
        type_majoration = ""

        if tarif_nuit:
            majoration_appliquee = self.majoration_nuit_weekend
            type_majoration = "nuit/weekend"

        if type_transport == TypeTransport.HOSPITALISATION.value:
            if distance_km < 50:
                maj_hosp = self.majoration_hospitalisation_courte
            else:
                maj_hosp = self.majoration_hospitalisation_longue

            if maj_hosp > majoration_appliquee:
                majoration_appliquee = maj_hosp
                type_majoration = f"hospitalisation ({'<50km' if distance_km < 50 else '>=50km'})"

        montant_majoration = base_tarifaire * majoration_appliquee
        total += montant_majoration

        # Suppléments
        supplements = 0.0
        if tpmr:
            supplements += self.supplement_tpmr
        if self.departement in self.departements_drom:
            supplements += self.supplement_drom
        supplements += peages

        # Transport partagé
        abattement_taux = 0.0
        abattement_montant = 0.0

        if nb_patients > 1:
            total_avant_supplements = total * nb_patients
            total = total_avant_supplements + supplements
            base_abattement = total - supplements + (self.supplement_tpmr if tpmr else 0)
            abattement_taux = self.abattements_partage.get(min(nb_patients, 4), self.abattements_partage[4])
            abattement_montant = base_abattement * abattement_taux
            total -= abattement_montant
        else:
            total += supplements

        return {
            "total": round(total, 2),
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
            "abattement_partage_montant": round(abattement_montant, 2)
        }

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
                           tarif_nuit: bool = False,
                           date_heure_transport: Optional[datetime] = None,
                           type_transport: TypeTransport = TypeTransport.SIMPLE,
                           nb_patients: int = 1,
                           tpmr: bool = False,
                           peages: float = 0.0):
        if date_heure_transport is None:
            date_heure_transport = datetime.now(pytz.timezone('Europe/Paris'))
        elif date_heure_transport.tzinfo is None:
            date_heure_transport = pytz.timezone('Europe/Paris').localize(date_heure_transport)

        # Déterminer si c'est tarif nuit (priorité au paramètre explicite)
        tarif_nuit_effectif = tarif_nuit
        if not tarif_nuit and date_heure_transport:
            tarif_nuit_effectif = (self.est_tarif_nuit(date_heure_transport.time()) or
                                 CalculateurTarifsCPAM.est_weekend_ou_ferie(date_heure_transport.date()))

        # Utiliser la méthode cachée pour le calcul de base
        resultat_cache = self._calculer_base_cpam(
            distance_km=distance_km,
            ville_depart=ville_depart,
            ville_arrivee=ville_arrivee,
            tarif_nuit=tarif_nuit_effectif,
            type_transport=type_transport.value,
            nb_patients=nb_patients,
            tpmr=tpmr,
            peages=peages
        )

        return {
            "total": resultat_cache["total"],
            "details": {
                "distance_km": distance_km,
                "nb_patients": nb_patients,
                "forfait_prise_charge": resultat_cache["forfait_prise_charge"],
                "forfait_grande_ville": resultat_cache["forfait_grande_ville"],
                "km_facturables": resultat_cache["km_facturables"],
                "tarif_km": resultat_cache["tarif_km"],
                "cout_kilometrique": resultat_cache["cout_kilometrique"],
                "base_tarifaire": resultat_cache["base_tarifaire"],
                "majoration_taux": resultat_cache["majoration_taux"],
                "majoration_type": resultat_cache["majoration_type"],
                "majoration_montant": resultat_cache["majoration_montant"],
                "supplement_tpmr": resultat_cache["supplement_tpmr"],
                "supplement_drom": resultat_cache["supplement_drom"],
                "peages": resultat_cache["peages"],
                "total_supplements": resultat_cache["total_supplements"],
                "abattement_partage_taux": resultat_cache["abattement_partage_taux"],
                "abattement_partage_montant": resultat_cache["abattement_partage_montant"],
                "departement": self.departement,
                "date_heure_transport": date_heure_transport.isoformat()
            }
        }