from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "")
if not SECRET_KEY:
    SECRET_KEY = "temporarysecretkeychangethisinproduction"
    print("WARNING: Using default JWT secret key. Set JWT_SECRET_KEY in .env file.")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 with Password flow
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")

# Define the router
auth_router = APIRouter(prefix="/auth", tags=["authentication"])

# Models
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: str = "user"  # Valeur par défaut

class UserInDB(BaseModel):
    username: str
    email: str
    hashed_password: str
    disabled: bool = False
    created_at: datetime = datetime.now()
    role: str = "user"  # Valeur par défaut

class User(BaseModel):
    username: str
    email: str
    disabled: bool = False
    role: str = "user"  # Ajouté ici aussi pour la réponse

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)
    disabled: Optional[bool] = None
    role: Optional[str] = None

# Helper functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# Dependency to get the database - MOVED UP
async def get_database():
    from main import mongo_client, db_name
    return mongo_client[db_name]

async def get_user(db: AsyncIOMotorDatabase, username: str):
    user_doc = await db.users.find_one({"username": username})
    if user_doc:
        return UserInDB(**user_doc)
    return None

async def authenticate_user(db: AsyncIOMotorDatabase, username: str, password: str):
    user = await get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncIOMotorDatabase = Depends(get_database)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Routes
@auth_router.post("/register", response_model=User)
async def register_user(user: UserCreate, db: AsyncIOMotorDatabase = Depends(get_database)):
    # Check if username already exists
    existing_user = await db.users.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email already exists
    existing_email = await db.users.find_one({"email": user.email})
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    user_in_db = UserInDB(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role
    )
    
    # Insert user into database
    await db.users.insert_one(user_in_db.dict())
    
    # Return user without hashed password
    return User(username=user.username, email=user.email)

@auth_router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncIOMotorDatabase = Depends(get_database)):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

# Route pour mettre à jour un utilisateur
@auth_router.put("/users/{username}", response_model=User)
async def update_user(
    username: str, 
    user_update: UserUpdate, 
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    # Vérifier les permissions: admins uniquement peuvent modifier les autres utilisateurs
    if current_user.username != username and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Vérifier si l'utilisateur existe
    user_db = await get_user(db, username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {username} not found"
        )
    
    # Construire la mise à jour
    update_data = {}
    if user_update.email:
        # Vérifier si l'email est déjà utilisé par un autre utilisateur
        existing_email = await db.users.find_one({"email": user_update.email, "username": {"$ne": username}})
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered to another user"
            )
        update_data["email"] = user_update.email
    
    if user_update.password:
        update_data["hashed_password"] = get_password_hash(user_update.password)
    
    # Seuls les admins peuvent modifier ces champs
    if current_user.role == "admin":
        if user_update.disabled is not None:
            update_data["disabled"] = user_update.disabled
        
        if user_update.role:
            update_data["role"] = user_update.role
    
    # Mettre à jour l'utilisateur s'il y a des modifications
    if update_data:
        await db.users.update_one(
            {"username": username},
            {"$set": update_data}
        )
    
    # Récupérer et retourner l'utilisateur mis à jour
    updated_user = await get_user(db, username)
    return User(
        username=updated_user.username,
        email=updated_user.email,
        disabled=updated_user.disabled,
        role=updated_user.role
    )

# Route pour supprimer un utilisateur
@auth_router.delete("/users/{username}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    username: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    # Vérifier les permissions: admins uniquement peuvent supprimer les autres utilisateurs
    if current_user.username != username and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Vérifier si l'utilisateur existe
    user = await get_user(db, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {username} not found"
        )
    
    # Empêcher la suppression du dernier admin
    if user.role == "admin":
        admin_count = await db.users.count_documents({"role": "admin"})
        if admin_count <= 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete the last admin user"
            )
    
    # Supprimer l'utilisateur
    result = await db.users.delete_one({"username": username})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete user"
        )
    
    return None  # 204 No Content, pas besoin de retourner de données

# Route pour lister tous les utilisateurs (admin uniquement)
@auth_router.get("/users", response_model=list[User])
async def list_users(
    skip: int = 0, 
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    # Vérifier que c'est un admin
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    users = []
    cursor = db.users.find().skip(skip).limit(limit)
    async for user_doc in cursor:
        user = UserInDB(**user_doc)
        users.append(User(
            username=user.username,
            email=user.email,
            disabled=user.disabled,
            role=user.role
        ))
    
    return users

# Route pour récupérer un utilisateur spécifique
@auth_router.get("/users/{username}", response_model=User)
async def get_user_by_username(
    username: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    # Vérifier les permissions: seul l'utilisateur lui-même ou un admin peut voir les détails
    if current_user.username != username and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    user = await get_user(db, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {username} not found"
        )
    
    return User(
        username=user.username,
        email=user.email,
        disabled=user.disabled,
        role=user.role
    )