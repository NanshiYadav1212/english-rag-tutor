from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from fastapi import APIRouter, HTTPException, Header
import os
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from app.db import db

router = APIRouter()

# Security config
SECRET = os.getenv("SECRET_KEY")
ALGO = os.getenv("ALGORITHM")
ACCESS_EXPIRE_MINUTES = int(os.getenv("ACCESS_EXPIRE_MINUTES", 1440))
pwd_ctx = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


# Schemas
class SignupIn(BaseModel):
    email: EmailStr
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Token creation
def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET, algorithm=ALGO)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGO])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db["users"].find_one({"email": payload.get("sub")})

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

# Get current user from Authorization header
# def get_current_user(authorization: str = Header(None)):
#     # Allow a development-only anonymous user when ALLOW_ANON=1
#     if not authorization:
#         if os.getenv("ALLOW_ANON") == "1":
#             return {"email": "dev@local", "level": "beginner"}
#         raise HTTPException(status_code=401, detail="Missing token")

#     try:
#         scheme, token = authorization.split()
#         if scheme.lower() != "bearer":
#             raise HTTPException(status_code=401, detail="Invalid token format")
#     except ValueError:
#         raise HTTPException(status_code=401, detail="Invalid authorization header")

#     try:
#         payload = jwt.decode(token, SECRET, algorithms=[ALGO])
#     except jwt.ExpiredSignatureError:
#         raise HTTPException(status_code=401, detail="Token expired")
#     except Exception:
#         raise HTTPException(status_code=401, detail="Invalid token")

#     user = db["users"].find_one({"email": payload.get("sub")})
    
#     if not user:
#         raise HTTPException(status_code=401, detail="User not found")

#     return user


# Signup
@router.post("/signup", response_model=TokenOut)
async def signup(payload: SignupIn):
    users = db["users"]

    if users.find_one({"email": payload.email}):
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = pwd_ctx.hash(payload.password)

    user = {
        "email": payload.email,
        "hashed_password": hashed,
        "level": "beginner",
        "created_at": datetime.utcnow()
    }

    users.insert_one(user)

    token = create_token({"sub": payload.email})

    return {"access_token": token}


# Login (JSON login)
@router.post("/login", response_model=TokenOut)
async def login(payload: SignupIn):
    users = db["users"]

    user = users.find_one({"email": payload.email})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not pwd_ctx.verify(payload.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({"sub": user["email"]})

    return {"access_token": token}
