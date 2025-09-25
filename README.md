# 🚕 API Taxi Vendée 2025 + CPAM

Une API REST moderne et complète pour calculer les tarifs de taxi en Vendée selon la réglementation officielle de 2025 ET les tarifs de transport sanitaire selon la convention-cadre nationale CPAM 2025.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/fastapi-0.117.1-green.svg)
![Version](https://img.shields.io/badge/version-1.0.0-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-production--ready-green.svg)

## 📋 Fonctionnalités

### 🚕 Tarifs Taxi Vendée 2025
- ✅ **Calcul de tarifs précis** basé sur les tarifs officiels Vendée 2025
- ✅ **Gestion des tarifs jour/nuit** (19h00-07h00)
- ✅ **Distinction aller simple / aller-retour**
- ✅ **Gestion des dimanches et jours fériés**
- ✅ **Calcul du temps d'attente**
- ✅ **Application du tarif minimum**

### 🏥 Tarifs CPAM Transport Sanitaire 2025
- ✅ **Calculs selon convention-cadre nationale CPAM 2025**
- ✅ **Forfaits de prise en charge** (€13.00 incluant 4 premiers km)
- ✅ **Suppléments grandes villes** (Paris, Lyon, Marseille, etc.)
- ✅ **Majorations nuit/weekend** (50%) et hospitalisation (25-50%)
- ✅ **Suppléments TPMR** (€30.00) et DROM (€3.00)
- ✅ **Abattements transport partagé** (23-37% selon nombre de patients)
- ✅ **Gestion des péages** et frais annexes

### 🛠️ Fonctionnalités techniques
- ✅ **Documentation API automatique** avec Swagger UI
- ✅ **Validation des données** avec Pydantic
- ✅ **API RESTful** avec FastAPI
- ✅ **Gestion des fuseaux horaires** (Europe/Paris)

## 🛠️ Stack Technique

- **Framework**: FastAPI 0.117.1
- **Langage**: Python 3.8+
- **Validation**: Pydantic 2.11.9
- **Serveur**: Uvicorn 0.37.0
- **Documentation**: Swagger UI automatique

## 🥰 Documentation

- [Swagger](https://api.b-tech.ovh/docs)
- [Redoc](https://api.b-tech.ovh/redoc)

## 😎 Demo

- [API Demo tarifs](https://api.b-tech.ovh/tarifs)


## 🚀 Installation

- Python 3.8 ou supérieur
- pip (gestionnaire de packages Python)

### Installation des dépendances

```bash
# Cloner le projet
git clone https://github.com/Glad91/taxi-fastapi-vendee.git
cd taxi-fastapi-vendee

# Installer les dépendances
pip install -r requirements.txt
```

### Lancement de l'application

```bash
# Démarrage en mode développement avec auto-reload
uvicorn main:app --reload

# Démarrage en production
uvicorn main:app --host 0.0.0.0 --port 8000
```

L'API sera accessible sur : `http://127.0.0.1:8000`

## 📖 Documentation

### Documentation interactive

Une fois l'application lancée, accédez à :

- **Swagger UI** : `http://127.0.0.1:8000/docs`
- **ReDoc** : `http://127.0.0.1:8000/redoc`

### Endpoints disponibles

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/verifier-sante` | GET | Vérification de l'état de l'API |
| `/calculer-tarif` | POST | **Taxi** - Calcul détaillé du tarif Vendée 2025 |
| `/calculer-tarif-cpam` | POST | **CPAM** - Calcul selon convention transport sanitaire 2025 |
| `/tarifs` | GET | Récupération des tarifs officiels taxi actuels |
| `/estimation-rapide` | GET | Estimation rapide taxi via paramètres URL |

## 💡 Utilisation

### 1. Vérification de l'état de l'API

```bash
curl -X GET "http://127.0.0.1:8000/verifier-sante"
```

**Réponse :**
```json
{
  "statut": "OK",
  "message": "API Taxi Tariff Calculator is running",
  "horodatage": "2025-09-23T21:18:48.392190"
}
```

### 2. Récupération des tarifs officiels

```bash
curl -X GET "http://127.0.0.1:8000/tarifs"
```

**Réponse :**
```json
{
  "prix_base": 2.94,
  "tarif_a_aller_retour_jour": 1.08,
  "tarif_b_aller_retour_nuit": 1.62,
  "tarif_c_simple_jour": 2.16,
  "tarif_d_simple_nuit": 3.24,
  "prix_par_minute_attente": 0.4906666666666667,
  "heures_de_nuit": "19:00:00 - 07:00:00",
  "tarif_minimum": 8.0
}
```

### 3. Estimation rapide

```bash
curl -X GET "http://127.0.0.1:8000/estimation-rapide?distance_km=10&aller_retour=true"
```

**Réponse :**
```json
{
  "distance_km": 10.0,
  "aller_retour": true,
  "total_estime": 28.74,
  "type_tarif": "nuit aller-retour (tarif B)"
}
```

### 4. Calcul détaillé Taxi

```bash
curl -X POST "http://127.0.0.1:8000/calculer-tarif" \
     -H "Content-Type: application/json" \
     -d '{
       "distance_km": 15.5,
       "duree_attente_minutes": 5,
       "aller_retour": true,
       "heure": "14:30",
       "date": "2025-09-23"
     }'
```

**Réponse :**
```json
{
  "prix_base": 2.94,
  "distance_km": 15.5,
  "distance_facturable": 31.0,
  "cout_distance": 50.22,
  "minutes_attente": 0.0,
  "cout_attente": 0.0,
  "type_tarif": "nuit aller-retour (tarif B)",
  "aller_retour": true,
  "tarif_km": 1.62,
  "tarif_minimum_applique": false,
  "total": 53.16,
  "date_heure_depart": "2025-09-23T21:20:13.347028"
}
```

### 5. Calcul CPAM Transport Sanitaire

```bash
curl -X POST "http://127.0.0.1:8000/calculer-tarif-cpam" \
     -H "Content-Type: application/json" \
     -d '{
       "distance_km": 25,
       "ville_depart": "La Roche-sur-Yon",
       "ville_arrivee": "Nantes",
       "date_heure_transport": "2025-01-15T21:30:00",
       "type_transport": "hospitalisation",
       "nb_patients": 2,
       "tpmr": true,
       "peages": 8.5,
       "departement": "85"
     }'
```

**Réponse :**
```json
{
  "total": 87.25,
  "details": {
    "forfait_prise_charge": 13.0,
    "distance_km": 25.0,
    "nb_patients": 2,
    "forfait_grande_ville": 15.0,
    "km_facturables": 21.0,
    "tarif_km": 1.07,
    "cout_kilometrique": 22.47,
    "base_tarifaire": 50.47,
    "majoration_taux": 0.5,
    "majoration_type": "nuit/weekend",
    "majoration_montant": 25.24,
    "supplement_tpmr": 30.0,
    "supplement_drom": 0.0,
    "peages": 8.5,
    "total_supplements": 38.5,
    "abattement_partage_taux": 0.23,
    "abattement_partage_montant": 26.07,
    "departement": "85",
    "date_heure_transport": "2025-01-15T21:30:00+01:00"
  }
}
```

## 📊 Système de Tarification

### Tarifs officiels Vendée 2025

| Type de Course | Tarif | Description |
|----------------|-------|-------------|
| **Tarif A** | 1,08 €/km | Aller-retour jour (lundi-samedi 07h00-19h00) |
| **Tarif B** | 1,62 €/km | Aller-retour nuit/dimanche/fériés |
| **Tarif C** | 2,16 €/km | Aller simple jour (lundi-samedi 07h00-19h00) |
| **Tarif D** | 3,24 €/km | Aller simple nuit/dimanche/fériés |

### Autres éléments tarifaires

- **Prix de base** : 2,94 € (prise en charge)
- **Temps d'attente** : 29,44 €/heure (0,49 €/minute)
- **Tarif minimum** : 8,00 €
- **Heures de nuit** : 19h00 - 07h00

### Logique de calcul aller-retour

- **Distance saisie** : Distance simple du trajet (ex: 45km)
- **Distance facturable** :
  - Aller simple : distance saisie (45km)
  - Aller-retour : distance saisie × 2 (90km)
- **Exemple** : Pour un aller-retour de 45km
  - Distance facturable : 90km
  - Coût : 90km × tarif aller-retour + prix de base

## 🏥 Système de Tarification CPAM 2025

### Tarifs selon convention-cadre nationale

| Élément | Tarif | Description |
|---------|-------|-------------|
| **Forfait prise en charge** | 13,00 € | Inclut les 4 premiers kilomètres |
| **Forfait grande ville** | 15,00 € | Supplément pour grandes métropoles |
| **Tarif kilométrique** | 1,07 €/km | À partir du 5ème kilomètre (Vendée) |

### Majorations CPAM

| Type | Taux | Conditions |
|------|------|------------|
| **Nuit/Weekend** | +50% | 20h00-08h00 et dimanches |
| **Hospitalisation courte** | +25% | Transport < 50 km |
| **Hospitalisation longue** | +50% | Transport ≥ 50 km |

### Suppléments

| Supplément | Montant | Description |
|------------|---------|-------------|
| **TPMR** | 30,00 € | Transport PMR avec véhicule adapté |
| **DROM** | 3,00 € | Départements d'Outre-Mer |
| **Péages** | Variable | Frais de péage réels |

### Abattements transport partagé

| Nombre de patients | Abattement | Description |
|-------------------|------------|-------------|
| **2 patients** | -23% | Réduction sur tarif de base |
| **3 patients** | -35% | Réduction sur tarif de base |
| **4+ patients** | -37% | Réduction maximale |

### Villes éligibles au forfait grande ville (15€)

- Paris, Marseille, Lyon, Toulouse, Nice, Nantes
- Strasbourg, Montpellier, Bordeaux, Lille, Rennes, Grenoble
- Départements 92, 93, 94 (Île-de-France)

### Logique de calcul CPAM

1. **Base** : 13€ forfait + éventuel forfait grande ville (15€)
2. **Kilométrage** : (distance - 4 km) × 1,07€/km
3. **Majorations** : Application de la plus élevée (nuit/weekend OU hospitalisation)
4. **Suppléments** : TPMR + DROM + péages
5. **Abattements** : Réduction selon nombre de patients (hors TPMR et péages)

## 🏗️ Architecture

```
taxi-fastapi-vendee/
├── main.py              # Application principale FastAPI
├── requirements.txt     # Dépendances Python
├── setup.py             # Configuration du package Python
├── pyproject.toml       # Configuration moderne du projet
├── test_main.http      # Tests HTTP manuels
├── conventions/         # Documents officiels CPAM
│   ├── convention_2024.pdf
│   └── convention_2025_nouvelle.pdf
├── CLAUDE.md           # Instructions pour Claude Code
├── LICENSE             # Licence MIT
└── README.md           # Cette documentation
```

### Structure du code

- **TypeTransport** (`main.py:10-12`) : Énumération pour types de transport CPAM
- **CalculateurTarifsTaxi** (`main.py:14-97`) : Logique métier taxi Vendée 2025
- **CalculateurTarifsCPAM** (`main.py:99-238`) : Logique métier transport sanitaire CPAM 2025
- **Modèles Pydantic Taxi** (`main.py:242-274`) : Validation taxi (CourseRequete, CourseReponse)
- **Modèles Pydantic CPAM** (`main.py:276-289`) : Validation CPAM (CourseCPAMRequete, CourseCPAMReponse)
- **Endpoints FastAPI** (`main.py:307-391`) : Points d'accès de l'API REST (5 endpoints)

## 🧪 Tests

### Tests manuels

Utilisez le fichier `test_main.http` avec votre IDE ou des outils comme Postman.

### Tests automatisés

```bash
# Lancement des tests (à implémenter)
pytest tests/
```

## 🚀 Déploiement

### Développement local

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 🌐 Déploiement gratuit sur Render

#### 1. Configuration automatique
Le projet inclut un fichier `render.yaml` pour un déploiement en 1 clic :

```yaml
services:
  - type: web
    name: taxi-api-vendee
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    healthCheckPath: /verifier-sante
```

#### 2. Déploiement étape par étape

1. **Créer un compte** sur [Render.com](https://render.com)

2. **Connecter le repository** :
   - Aller sur le dashboard Render
   - Cliquer "New +" → "Web Service"
   - Connecter votre compte GitHub
   - Sélectionner le repo `taxi-fastapi-vendee`

3. **Configuration automatique** :
   - Render détecte automatiquement le `render.yaml`
   - Nom : `taxi-api-vendee`
   - Build Command : `pip install -r requirements.txt`
   - Start Command : `uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **Déployer** :
   - Cliquer "Create Web Service"
   - Le déploiement prend 2-3 minutes
   - URL finale : `https://tarif-taxi-vendee.onrender.com`

#### 3. Test en production

Une fois déployé, tester avec :
```bash
curl https://tarif-taxi-vendee.onrender.com/verifier-sante
```

#### 4. Limitations du plan gratuit

- ⏰ **Hibernation** : L'app s'endort après 15min d'inactivité
- 🔄 **Réveil** : Premier accès prend ~30 secondes
- ⚡ **750h/mois** incluses (suffisant pour la plupart des usages)

### Production alternative

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker (optionnel)

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📝 Exemples d'utilisation

### Python avec requests

```python
import requests

# Estimation rapide taxi
response = requests.get(
    "http://127.0.0.1:8000/estimation-rapide",
    params={"distance_km": 12.5, "aller_retour": True}
)
print(response.json())

# Calcul détaillé taxi
data = {
    "distance_km": 20.0,
    "minutes_attente": 3.0,
    "aller_retour": False,
    "date_heure_depart": "2025-09-23T22:30:00"
}
response = requests.post(
    "http://127.0.0.1:8000/calculer-tarif",
    json=data
)
print(response.json())

# Calcul CPAM transport sanitaire
cpam_data = {
    "distance_km": 45.0,
    "ville_depart": "Vendée",
    "ville_arrivee": "Paris",
    "date_heure_transport": "2025-01-20T14:30:00",
    "type_transport": "simple",
    "nb_patients": 3,
    "tpmr": False,
    "peages": 12.5,
    "departement": "85"
}
cpam_response = requests.post(
    "http://127.0.0.1:8000/calculer-tarif-cpam",
    json=cpam_data
)
print(cpam_response.json())
```

### JavaScript avec fetch

```javascript
// Estimation rapide taxi
const response = await fetch(
  'http://127.0.0.1:8000/estimation-rapide?distance_km=8&aller_retour=false'
);
const data = await response.json();
console.log(data);

// Calcul détaillé taxi
const calculation = await fetch('http://127.0.0.1:8000/calculer-tarif', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    distance_km: 15.0,
    minutes_attente: 2.0,
    aller_retour: true
  })
});
const result = await calculation.json();
console.log(result);

// Calcul CPAM transport sanitaire
const cpamCalculation = await fetch('http://127.0.0.1:8000/calculer-tarif-cpam', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    distance_km: 30.0,
    ville_depart: "La Roche-sur-Yon",
    ville_arrivee: "Lyon",
    date_heure_transport: "2025-02-15T09:00:00",
    type_transport: "hospitalisation",
    nb_patients: 1,
    tpmr: true,
    peages: 20.0,
    departement: "85"
  })
});
const cpamResult = await cpamCalculation.json();
console.log(cpamResult);
```

## 🤝 Contribution

1. Forkez le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Committez vos changements (`git commit -am 'Ajout nouvelle fonctionnalité'`)
4. Poussez vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Ouvrez une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 👨‍💻 Auteur

Développé avec ❤️ pour la gestion des tarifs de taxi en Vendée.

## 🔗 Liens utiles

- [Repository GitHub](https://github.com/Glad91/taxi-fastapi-vendee)
- [Documentation de l'API](https://github.com/Glad91/taxi-fastapi-vendee#endpoints-disponibles)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)
- [Uvicorn Documentation](https://www.uvicorn.org/)

---

🤖 *Généré avec [Claude Code](https://claude.ai/code)*

*Co-Authored-By: Claude <noreply@anthropic.com>*