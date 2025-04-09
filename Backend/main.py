from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
import uvicorn
import os
from dotenv import load_dotenv
import json

# Import the auth router
from auth import auth_router
from protected_routes import protected_router
from plant import plants_router

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="E-Garden Smart Gardening System")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ppe-puce.vercel.app", "http://localhost:3000"],  # In production, limit to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB configuration
uri = os.getenv("MONGODB_URL", "").strip()
db_name = os.getenv("MONGODB_DB", "").strip()

# Global MongoDB client
mongo_client = AsyncIOMotorClient(uri, server_api=ServerApi('1'))

# Startup event: connect to MongoDB
@app.on_event("startup")
async def startup_db_client():
    try:
        # Send a ping to confirm a successful connection
        await mongo_client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        print("Routes disponibles:")
        for route in app.routes:
            print(f"{route.path} - {route.methods}")
    except Exception as e:
        print(e)

# Shutdown event: close MongoDB connection
@app.on_event("shutdown")
async def shutdown_db_client():
    global mongo_client
    if mongo_client:
        mongo_client.close()
        print("MongoDB connection closed")

# Dependency to get the database
async def get_database():
    if mongo_client is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection not available"
        )
    return mongo_client[db_name]

# Include the auth router
app.include_router(auth_router)
# Include the protected router
app.include_router(protected_router)
# Include the plant router
app.include_router(plants_router)

# API routes
@app.get("/")
def read_root():
    return {"message": "Welcome to E-Garden Smart Gardening System!"}


@app.get("/mongodb")
async def test_mongodb(db=Depends(get_database)):
    try:
        # Test connection by listing collections
        collections = await db.list_collection_names()
        print(f"Connected to database: {db_name}")
        print(f"Collections found: {collections}")
        return {
            "status": "success",
            "collections": collections,
            "message": "Successfully connected to MongoDB!"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"MongoDB connection error: {str(e)}"
        )
    
@app.post("/users/test")
async def create_test_user(user_data: dict, db=Depends(get_database)):
    try:
        collection = db["users"]
        
        # Check if username already exists
        existing_user = await collection.find_one({"username": user_data["username"]})
        if existing_user:
            return {
                "status": "error",
                "message": f"Username '{user_data['username']}' already exists"
            }
        
        # Insert the new user
        result = await collection.insert_one(user_data)
        
        return {
            "status": "success",
            "message": f"Test user '{user_data['username']}' created successfully",
            "user_id": str(result.inserted_id)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error creating test user: {str(e)}"
        }
    
@app.get("/users")
async def get_all_users(db=Depends(get_database)):
    try:
        collection = db["users"]
        
        # Fetch all users
        users = await collection.find().to_list(length=None)
        
        # Convert ObjectId to string
        for user in users:
            user["_id"] = str(user["_id"])
        
        return {
            "status": "success",
            "users": users
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error fetching users: {str(e)}"
        }


# Entry point
if __name__ == "__main__":
    # Start the FastAPI app with Uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)