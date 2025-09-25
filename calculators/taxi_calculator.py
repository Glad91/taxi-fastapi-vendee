from datetime import datetime, time, date
from typing import Optional
import pytz


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