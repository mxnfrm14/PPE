from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Initialisation de l'application FastAPI
app = FastAPI(title="Système d'arrosage intelligent")

# Configuration CORS pour permettre les requêtes depuis votre frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, limitez aux domaines spécifiques
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes de l'API
@app.get("/api")
def read_root():
    return {"message": "Bienvenue dans le système d'arrosage intelligent!"}


# Point de départ - SANS Ngrok maintenant
if __name__ == "__main__":
    # Démarrer l'application FastAPI avec Uvicorn
    # Écoute sur toutes les interfaces pour être accessible via Tailscale
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)