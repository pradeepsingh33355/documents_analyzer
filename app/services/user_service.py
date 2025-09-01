from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import User
from app.schemas import schemas
from app.core.security import get_password_hash, verify_password
from app.core.config import settings
from typing import Optional, List
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], default="bcrypt")


async def create_initial_admin():
    """Create the admin user if it doesn't exist"""
    db = SessionLocal()
    admin = get_user_by_email(db, settings.ADMIN_EMAIL)
    if not admin:
        admin = User(
            username=settings.ADMIN_USERNAME,
            email=settings.ADMIN_EMAIL,
            hashed_password=get_password_hash(settings.ADMIN_PASSWORD),
            is_admin=True,
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)

    db.close()
    return admin


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = db.query(User).filter(User.email == email).first()

    if user and pwd_context.verify(password, user.hashed_password):
        return user
