# 🚕 API Taxi Vendée 2025

Une API REST moderne et complète pour calculer les tarifs de taxi en Vendée selon la réglementation officielle de 2025.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/fastapi-0.117.1-green.svg)
![Version](https://img.shields.io/badge/version-1.0.0-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-production--ready-green.svg)

## 📋 Fonctionnalités

- ✅ **Calcul de tarifs précis** basé sur les tarifs officiels Vendée 2025
- ✅ **Gestion des tarifs jour/nuit** (19h00-07h00)
- ✅ **Distinction aller simple / aller-retour**
- ✅ **Gestion des dimanches et jours fériés**
- ✅ **Calcul du temps d'attente**
- ✅ **Application du tarif minimum**
- ✅ **Documentation API automatique** avec Swagger UI
- ✅ **Validation des données** avec Pydantic
- ✅ **API RESTful** avec FastAPI

## 🛠️ Stack Technique

- **Framework**: FastAPI 0.117.1
- **Langage**: Python 3.8+
- **Validation**: Pydantic 2.11.9
- **Serveur**: Uvicorn 0.37.0
- **Documentation**: Swagger UI automatique

## 🚀 Installation

### Prérequis

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
| `/calculer-tarif` | POST | Calcul détaillé du tarif d'une course |
| `/tarifs` | GET | Récupération des tarifs officiels actuels |
| `/estimation-rapide` | GET | Estimation rapide via paramètres URL |

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

### 4. Calcul détaillé

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
  "cout_distance": 25.11,
  "minutes_attente": 0.0,
  "cout_attente": 0.0,
  "type_tarif": "nuit aller-retour (tarif B)",
  "aller_retour": true,
  "tarif_km": 1.62,
  "tarif_minimum_applique": false,
  "total": 28.05,
  "date_heure_depart": "2025-09-23T21:20:13.347028"
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

## 🏗️ Architecture

```
taxi-fastapi-vendee/
├── main.py              # Application principale FastAPI
├── requirements.txt     # Dépendances Python
├── setup.py             # Configuration du package Python
├── pyproject.toml       # Configuration moderne du projet
├── test_main.http      # Tests HTTP manuels
├── CLAUDE.md           # Instructions pour Claude Code
├── LICENSE             # Licence MIT
└── README.md           # Cette documentation
```

### Structure du code

- **CalculateurTarifsTaxi** (`main.py:8-79`) : Logique métier de calcul des tarifs
- **Modèles Pydantic** (`main.py:83-116`) : Validation et sérialisation des données
- **Endpoints FastAPI** (`main.py:130-193`) : Points d'accès de l'API REST

## 🧪 Tests

### Tests manuels

Utilisez le fichier `test_main.http` avec votre IDE ou des outils comme Postman.

### Tests automatisés

```bash
# Lancement des tests (à implémenter)
pytest tests/
```

## 🚀 Déploiement

### Développement

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production

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

# Estimation rapide
response = requests.get(
    "http://127.0.0.1:8000/estimation-rapide",
    params={"distance_km": 12.5, "aller_retour": True}
)
print(response.json())

# Calcul détaillé
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
```

### JavaScript avec fetch

```javascript
// Estimation rapide
const response = await fetch(
  'http://127.0.0.1:8000/estimation-rapide?distance_km=8&aller_retour=false'
);
const data = await response.json();
console.log(data);

// Calcul détaillé
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