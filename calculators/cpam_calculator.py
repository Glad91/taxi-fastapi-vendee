from datetime import datetime, time, date
from typing import Optional
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