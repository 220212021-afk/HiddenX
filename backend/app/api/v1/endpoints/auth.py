from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.auth import RegisterIn, LoginIn, TokenOut
from app.schemas.user import UserPublic
from app.services import auth_service
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def register(data: RegisterIn, db: AsyncSession = Depends(get_db)):
    return await auth_service.register(db, data)

@router.post("/login", response_model=TokenOut)
async def login(data: LoginIn, db: AsyncSession = Depends(get_db)):
    token = await auth_service.login(db, data)
    return TokenOut(
        access_token=token,
        expires_in=settings.access_token_expire_minutes * 60
    )
