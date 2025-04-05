from fastapi import APIRouter, HTTPException, Depends, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional
from bson.objectid import ObjectId
from auth import get_current_active_user, User

# Create a router with the /api prefix
plants_router = APIRouter(prefix="/plant", tags=["plants"])

# Models
class SemisBase(BaseModel):
    nom: str = Field(..., min_length=1, max_length=50, description="Name of the plant")
    date_plantation: str = Field(..., description="Date of plantation (YYYY-MM-DD)")
    place: int = Field(..., ge=1, le=12, description="Position in the grid (1-12)")
    dernier_arrosage: Optional[str] = Field(None, description="Last watering date (optional)")

class SemisCreate(SemisBase):
    pass

class SemisUpdate(BaseModel):
    nom: Optional[str] = Field(None, min_length=1, max_length=50, description="Name of the plant")
    date_plantation: Optional[str] = Field(None, description="Date of plantation (YYYY-MM-DD)")
    dernier_arrosage: Optional[str] = Field(None, description="Last watering date (optional)")
    place: Optional[int] = Field(None, ge=1, le=12, description="Position in the grid (1-12)")
    
# class WateringBase(BaseModel):
#     semis_id: str = Field(..., description="ID of the semis")
#     date_arrosage: str = Field(..., description="Date and time of watering (ISO format)")
#     quantite_eau_ml: int = Field(..., gt=0, le=1000, description="Amount of water in milliliters")

class WateringBase(BaseModel):
    plantId: str
    dateTime: str
    duration: int = Field(..., gt=0, le=60, description="Duration in minutes")
    amount: int = Field(..., gt=0, le=1000, description="Amount in milliliters")

class WateringCreate(WateringBase):
    pass

class WateringResponse(WateringBase):
    id: str
    created_at: Optional[str] = None

# Helper function to get database
async def get_database():
    from main import mongo_client, db_name
    return mongo_client[db_name]

# Routes
@plants_router.get("/semis")
async def get_all_plants(
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get all plants from the semis collection"""
    # Fetch all plants
    plants = []
    cursor = db.semis.find().sort("place", 1)
    
    async for plant in cursor:
        # Convert MongoDB _id to string
        plant["_id"] = str(plant["_id"])
        plants.append(plant)
    
    return plants

@plants_router.get("/semis/{plant_id}")
async def get_plant_by_id(
    plant_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get a specific plant by ID"""
    try:
        plant_obj_id = ObjectId(plant_id)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ID format"
        )
    
    # Fetch the plant
    plant = await db.semis.find_one({"_id": plant_obj_id})
    
    if not plant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plant with ID {plant_id} not found"
        )
    
    # Convert MongoDB _id to string
    plant["_id"] = str(plant["_id"])
    
    return plant

@plants_router.post("/semis", status_code=status.HTTP_201_CREATED)
async def create_semis(
    semis: SemisCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Create a new semis entry"""
    # Check if the position is already taken
    existing_place = await db.semis.find_one({"place": semis.place})
    if existing_place:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Position {semis.place} is already occupied by another plant"
        )
    
    # Prepare the semis record
    semis_data = semis.dict()
    semis_data["created_at"] = datetime.now().isoformat()
    semis_data["created_by"] = current_user.username
    
    # Initialize humidity level (random initial value between 40-60%)
    import random
    semis_data["txHumidMesure"] = random.randint(40, 60)
    
    # Insert the record
    result = await db.semis.insert_one(semis_data)
    
    # Return the created semis with its ID
    created_semis = await db.semis.find_one({"_id": result.inserted_id})
    created_semis["_id"] = str(created_semis["_id"])
    
    return created_semis

@plants_router.put("/semis/{semis_id}", status_code=status.HTTP_200_OK)
async def update_semis(
    semis_id: str,
    semis_update: SemisUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Update an existing semis entry"""
    try:
        semis_obj_id = ObjectId(semis_id)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ID format"
        )
    
    # Verify semis exists
    existing_semis = await db.semis.find_one({"_id": semis_obj_id})
    if not existing_semis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Semis with ID {semis_id} not found"
        )
    
    # Check if trying to update to a place that's already taken by another semis
    if semis_update.place is not None and semis_update.place != existing_semis.get("place"):
        place_taken = await db.semis.find_one({
            "place": semis_update.place,
            "_id": {"$ne": semis_obj_id}
        })
        if place_taken:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Position {semis_update.place} is already occupied by another plant"
            )
    
    # Prepare the update data (only include fields that are provided)
    update_data = {}
    for key, value in semis_update.dict(exclude_unset=True).items():
        if value is not None:  # Only include fields with non-None values
            update_data[key] = value
    
    # Add updated_at timestamp
    update_data["updated_at"] = datetime.now().isoformat()
    update_data["updated_by"] = current_user.username
    
    # Update the semis
    await db.semis.update_one(
        {"_id": semis_obj_id},
        {"$set": update_data}
    )
    
    # Return the updated semis
    updated_semis = await db.semis.find_one({"_id": semis_obj_id})
    updated_semis["_id"] = str(updated_semis["_id"])
    
    return updated_semis

@plants_router.delete("/semis/{semis_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_semis(
    semis_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Delete a semis entry"""
    try:
        semis_obj_id = ObjectId(semis_id)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ID format"
        )
    
    # Verify semis exists
    existing_semis = await db.semis.find_one({"_id": semis_obj_id})
    if not existing_semis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Semis with ID {semis_id} not found"
        )
    
    # Delete any associated watering records
    await db.arrosages.delete_many({"semis_id": semis_id})
    
    # Delete the semis
    await db.semis.delete_one({"_id": semis_obj_id})
    
    # No content returned for successful deletion
    return None

@plants_router.get("/infos/{plant_type}")
async def get_plant_info(
    plant_type: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get detailed information about a specific plant type from the infos collection"""
    # Fetch the plant info
    plant_info = await db.infos.find_one({"name": plant_type})
    
    if not plant_info:
        # Try case-insensitive search
        cursor = db.infos.find({"name": {"$regex": f"^{plant_type}$", "$options": "i"}})
        async for doc in cursor:
            plant_info = doc
            break
    
    if not plant_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plant info for '{plant_type}' not found"
        )
    
    # Convert MongoDB _id to string
    plant_info["_id"] = str(plant_info["_id"])
    
    return plant_info

@plants_router.get("/arrosages/{semis_id}")
async def get_watering_history(
    semis_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get watering history for a specific plant"""
    try:
        ObjectId(semis_id)  # Validate ID format
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid semis ID format"
        )
    
    # Fetch watering records
    watering_records = []
    cursor = db.arrosages.find({"semis_id": semis_id}).sort("date_arrosage", -1)
    
    async for record in cursor:
        # Convert MongoDB _id to string
        record["_id"] = str(record["_id"])
        watering_records.append(record)
    
    return watering_records

@plants_router.post("/arrosages", status_code=status.HTTP_201_CREATED)
async def water_plant(
    watering: WateringCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Add a new watering record"""
    try:
        plant_obj_id = ObjectId(watering.semis_id)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid semis ID format"
        )
    
    # Verify plant exists
    plant = await db.semis.find_one({"_id": plant_obj_id})
    if not plant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Semis with ID {watering.semis_id} not found"
        )
    
    # Prepare the watering record
    watering_record = watering.dict()
    watering_record["created_at"] = datetime.now().isoformat()
    watering_record["created_by"] = current_user.username
    
    # Insert the record
    result = await db.arrosages.insert_one(watering_record)
    
    # Update plant's last watering info and humidity level
    # Simulate humidity increasing after watering
    current_humidity = plant.get("txHumidMesure", 0)
    humidity_increase = min(30, 100 - current_humidity)  # Increase by up to 30%, max 100%
    
    await db.semis.update_one(
        {"_id": plant_obj_id},
        {
            "$set": {
                "dernier_arrosage": watering.date_arrosage,
                "txHumidMesure": current_humidity + humidity_increase
            }
        }
    )
    
    # Return success
    return {
        "status": "success",
        "message": "Arrosage enregistré avec succès",
        "id": str(result.inserted_id)
    }