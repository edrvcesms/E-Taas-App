from passlib.context import CryptContext
from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError
import datetime
from .config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password with bcrypt (max 72 bytes)."""
    truncated = password.encode("utf-8")[:72].decode("utf-8", errors="ignore")
    return pwd_context.hash(truncated)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    truncated = plain_password.encode("utf-8")[:72].decode("utf-8", errors="ignore")
    return pwd_context.verify(truncated, hashed_password)

ACCESS_TOKEN_EXPIRE_DAYS = 1
REFRESH_TOKEN_EXPIRE_DAYS = 7

def create_access_token(data: dict, secret_key: str, algorithm: str = settings.ALGORITHM) -> str:
    payload = data.copy()
    payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    payload["type"] = "access"
    return encode(payload, secret_key, algorithm=algorithm)

def create_refresh_token(data: dict, secret_key: str, algorithm: str = settings.ALGORITHM) -> str:
    payload = data.copy()
    payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    payload["type"] = "refresh"
    return encode(payload, secret_key, algorithm=algorithm)

def decode_token(token: str, secret_key: str, algorithms: list = [settings.ALGORITHM]) -> dict:
    try:
        payload = decode(token, secret_key, algorithms=algorithms)
        return payload
    except ExpiredSignatureError:
        raise Exception("Token expired")
    except InvalidTokenError:
        raise Exception("Invalid token")

def is_token_valid(token: str, secret_key: str, algorithms: list = [settings.ALGORITHM]) -> bool:
    try:
        decode(token, secret_key, algorithms=algorithms)
        return True
    except (ExpiredSignatureError, InvalidTokenError):
        return False