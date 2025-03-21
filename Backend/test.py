from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient  # Utilise Motor pour MongoDB asynchrone
from pymongo.server_api import ServerApi
import uvicorn
import os
from dotenv import load_dotenv
import json

# Charger les variables d'environnement
load_dotenv()

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

# Configuration MongoDB
uri = os.getenv("MONGODB_URL", "").strip()
db_name = os.getenv("MONGODB_DB", "").strip()

# Client MongoDB global (AsyncIOMotorClient)
mongo_client = AsyncIOMotorClient(uri, server_api=ServerApi('1'))

# Événement de démarrage: se connecter à MongoDB
@app.on_event("startup")
async def startup_db_client():
    try:
        # Send a ping to confirm a successful connection
        await mongo_client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

# Événement d'arrêt: fermer la connexion à MongoDB
@app.on_event("shutdown")
async def shutdown_db_client():
    global mongo_client
    if mongo_client:
        mongo_client.close()
        print("MongoDB connection closed")

# Dépendance pour obtenir la base de données
async def get_database():
    if mongo_client is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection not available"
        )
    return mongo_client[db_name]

# Routes de l'API
@app.get("/api")
def read_root():
    return {"message": "Bienvenue dans le système d'arrosage intelligent!"}

@app.get("/api/mongodb")
async def test_mongodb(db=Depends(get_database)):
    try:
        # Tester la connexion en listant les collections (asynchrone avec Motor)
        collections = await db.list_collection_names() 
        print(f"Connexion à la base de données : {db_name}")
        print(f"Collections trouvées : {collections}") # Cela fonctionne avec Motor
        return {
            "status": "connected",
            "collections": collections,
            "message": "Connexion à MongoDB réussie!"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur de connexion à MongoDB: {str(e)}"
        )
    
    
@app.post("/api/test-insertion")
async def test_insertion(db=Depends(get_database)):
    try:
        collection = db["test"]  # Crée une collection appelée "test"
        result = await collection.insert_one({"name": "test", "value": 123})
        return {"status": "inserted", "document_id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'insertion : {str(e)}"
        )
    
@app.get("/api/test")
async def test(db=Depends(get_database)):
    try:
        collection = db["test"]  # Utiliser la collection "test"
        data = await collection.find().to_list(length=None)
        # Convertir les documents BSON en JSON
        data = json.loads(json.dumps(data, default=str))
        # Afficher les données dans la console
        print(f"Data retrieved: {data}")
        # Retourner les données au client
        return {"data": data}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des données : {str(e)}"
        )


# Point de départ
if __name__ == "__main__":
    # Démarrer l'application FastAPI avec Uvicorn
    uvicorn.run("test:app", host="0.0.0.0", port=8000, reload=True)
