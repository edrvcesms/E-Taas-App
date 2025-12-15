from passlib.context import CryptContext
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta
from core.config import settings

JWT_SECRET = settings.SECRET_KEY
JWT_ALGORITHM = settings.ALGORITHM
JWT_EXPIRATION_MINUTES = settings.JWT_EXPIRATION_MINUTES


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_token(token: str, secret_key: str, algorithms: list) -> dict:
    try:
        payload = jwt.decode(token, secret_key, algorithms=algorithms)
        return payload
    except (ExpiredSignatureError, InvalidTokenError):
        return None
    
def is_token_valid(token: str, secret_key: str, algorithms: list) -> bool:
    try:
        jwt.decode(token, secret_key, algorithms=algorithms)
        return True
    except (ExpiredSignatureError, InvalidTokenError):
        return False
