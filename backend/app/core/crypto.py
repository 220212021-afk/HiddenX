import hashlib
import hmac

from cryptography.fernet import Fernet

from app.core.config import settings

_fernet = Fernet(settings.encryption_key.encode())


def normalize_email(email: str) -> str:
    return email.strip().lower()


def encrypt(text: str) -> str:
    return _fernet.encrypt(text.encode()).decode()


def decrypt(token: str) -> str:
    return _fernet.decrypt(token.encode()).decode()


def hash_email(email: str) -> str:
    digest = hmac.new(
        settings.hmac_key.encode(),
        normalize_email(email).encode(),
        hashlib.sha256,
    )
    return digest.hexdigest()
