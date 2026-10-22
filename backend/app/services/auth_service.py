from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.crypto import encrypt, hash_email, normalize_email
from app.core.exceptions import ConflictError
from app.core.security import hash_password
from app.models.user import User
from app.schemas.auth import RegisterIn
from app.utils.anon_id import generate_anon_id

async def register(db: AsyncSession, data: RegisterIn) -> User():
    email_hash = hash_email(data.email)

    existing = await db.scalar(select(User.id).where(User.email_hash == email_hash))
    if existing is not None:
        raise ConflictError("Email Sudah terdaftar", code="EMAIL_TAKEN")

    for i in range(5):
        anon_id = generate_anon_id()
        taken = await db.scalar(select(User.id). where(User.anon_id == anon_id))
        if taken is None:
            break
    else:
        raise ConflictError("gagal membuat anon id, silakan coba lagi", code="ANON_ID_UNAVAILABLE")

    user = User(
            anon_id=anon_id,
            email_enc=encrypt(normalize_email(data.email)),
            email_hash=email_hash,
            password_hash=hash_password(data.password),
        )

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
