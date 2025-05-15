from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt

# This is for demo only. NEVER hardcode in production.
JWT_SECRET = "supersecret"
JWT_ALGORITHM = "HS256"

router = APIRouter()

# In-memory "database"
users = {}

class RegisterInput(BaseModel):
    username: str
    password: str

class LoginInput(BaseModel):
    username: str
    password: str

@router.post("/register")
def register(input: RegisterInput):
    if input.username in users:
        raise HTTPException(status_code=400, detail="User already exists")
    users[input.username] = input.password
    return {"message": "✅ Registered successfully"}

@router.post("/login")
def login(input: LoginInput):
    if users.get(input.username) != input.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    payload = {
        "sub": input.username,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return {"access_token": token}
