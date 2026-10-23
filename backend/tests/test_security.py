from app.core.crypto import decrypt, encrypt, hash_email
from app.core.security import hash_password, verify_password


def test_password_hash_and_verify():
    hashed = hash_password("rahasia123")
    assert hashed != "rahasia123"
    assert verify_password("rahasia123", hashed) is True
    assert verify_password("salah", hashed) is False


def test_email_encryption_roundtrip():
    assert decrypt(encrypt("a@b.com")) == "a@b.com"


def test_email_hash_is_consistent_after_normalization():
    assert hash_email(" User@Example.com ") == hash_email("user@example.com")
