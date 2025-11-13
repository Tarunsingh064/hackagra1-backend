from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.user import UserCreate, UserOut
from app.db.collections.user_collection import create_user, get_user_by_email
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter()

@router.post("/register", response_model=UserOut)
async def register(user: UserCreate):
    existing = await get_user_by_email(user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_data = {
        "username": user.username,
        "email": user.email,
        "hashed_password": hash_password(user.password),
    }
    user_id = await create_user(user_data)
    return {"id": user_id, "username": user.username, "email": user.email}

@router.post("/login")
async def login(user: UserCreate):
    db_user = await get_user_by_email(user.email)
    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
