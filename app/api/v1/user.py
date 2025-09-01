from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from app.core.config import settings
from app.schemas.schemas import UserLogin
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.user_service import authenticate_user
from app.core.security import create_access_token
from datetime import timedelta

router = APIRouter()


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(data: UserLogin, db: Session = Depends(get_db)):

    user = authenticate_user(db, data.email, data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired OTP")

    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS),
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "email": user.email,
        "name": user.username,
        "is_admin": user.is_admin,
    }
