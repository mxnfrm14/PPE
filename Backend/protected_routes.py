# Créez un fichier comme protected_routes.py
from fastapi import APIRouter, Depends
from auth import get_current_active_user
from temperature_service import temperature_service

# Créer un routeur avec une dépendance globale
protected_router = APIRouter(
    prefix="/protected",
    tags=["protected"],
    dependencies=[Depends(get_current_active_user)],
    responses={401: {"description": "Non autorisé"}},
)

@protected_router.get("/data")
async def get_data():
    # Tous les endpoints de ce routeur sont protégés
    return {"message": "Données protégées"}

@protected_router.get("/temperature")
async def get_temperature():
    # Endpoint protégé pour obtenir la température
    data = temperature_service.read_temperature()
    return data
    # return {"temperature": 22.5}
