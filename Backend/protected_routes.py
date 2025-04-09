from fastapi import APIRouter, Depends
from auth import get_current_active_user
from temperature_service import temperature_service
from humidity_service import humidity_service

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

@protected_router.get("/humidity")
async def get_all_humidity():
    """Endpoint to get humidity readings for all sensors"""
    data = humidity_service.read_humidity()
    return data

@protected_router.get("/humidity/{place}")
async def get_humidity_by_place(place: int):
    """Endpoint to get humidity reading for a specific place"""
    data = humidity_service.read_humidity(place)
    return data
