from webbrowser import get
import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import UnauthorizedError
from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.user import User, UserStatus

bearer_scheme = HTTPBearer(auto_error=False)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    if credentials is None:
        raise UnauthorizedError("token tidak ditemukan", code="TOKEN_MISSING")

    try:
        payload = decode_access_token(credentials.credentials)
    except jwt.ExpiredSignatureError:
        raise UnauthorizedError("token kadaluwarsa", code="TOKEN_EXPIRED")
    except jwt.InvalidTokenError:
        raise UnauthorizedError("token tidak valid", code="TOKEN_INVALID")

    user = await db.get(User, int(payload["sub"]))
    if user is None or user.status != UserStatus.active:
        raise UnauthorizedError("akun tidak valid", code="USER_INACTIVE")

    return user
