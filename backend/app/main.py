"""Point d'entree de l'API FastAPI.

Ce module reste volontairement fin : il assemble l'application, applique les
middlewares transverses, puis monte les routes versionnees par le prefixe de
configuration. La logique metier vit dans `services/`, et l'acces aux donnees
dans `repositories/`, afin de pouvoir remplacer les CSV par SQL sans toucher a
la couche HTTP.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.core.config import get_settings


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Backend API for the CCPNA CMR dashboard migration.",
)

# Le frontend Vite local appelle l'API directement pendant le developpement.
# En Docker/production, Nginx proxifie `/api` et le CORS devient surtout utile
# pour conserver une experience de dev simple.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Toutes les routes applicatives sont exposees sous `/api` par defaut. Le
# prefixe est centralise dans la configuration pour rester modifiable si l'API
# doit un jour cohabiter avec d'autres services.
app.include_router(router, prefix=settings.api_prefix)
