from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from routes import health, taxi, cpam

# --- Initialisation de l'API ---

app = FastAPI(
    title="API Taxi Vendée 2025 + CPAM",
    description="Une API pour calculer les tarifs de taxi en Vendée ET les tarifs de transport sanitaire selon la convention-cadre nationale CPAM 2025. La documentation est générée automatiquement par FastAPI.",
    version="1.0.0",
)

# --- Middlewares pour les performances ---

# Compression GZip pour réduire la taille des réponses (gain ~70%)
app.add_middleware(GZipMiddleware, minimum_size=500)

# --- Enregistrement des routes ---

app.include_router(health.router, tags=["Santé"])
app.include_router(taxi.router, tags=["Taxi Vendée"])
app.include_router(cpam.router, tags=["CPAM Transport Sanitaire"])


# Pour lancer l'application en ligne de commande :
# uvicorn main:app --reload