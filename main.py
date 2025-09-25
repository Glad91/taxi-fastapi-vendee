from fastapi import FastAPI
from routes import health, taxi, cpam

# --- Initialisation de l'API ---

app = FastAPI(
    title="API Taxi Vendée 2025 + CPAM",
    description="Une API pour calculer les tarifs de taxi en Vendée ET les tarifs de transport sanitaire selon la convention-cadre nationale CPAM 2025. La documentation est générée automatiquement par FastAPI.",
    version="1.0.0",
)

# --- Enregistrement des routes ---

app.include_router(health.router, tags=["Santé"])
app.include_router(taxi.router, tags=["Taxi Vendée"])
app.include_router(cpam.router, tags=["CPAM Transport Sanitaire"])


# Pour lancer l'application en ligne de commande :
# uvicorn main:app --reload