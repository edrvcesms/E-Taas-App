from passlib.context import CryptContext
from jwt import encode, decode, PyJWTError
from firebase_admin import auth
from firebase_admin.auth import InvalidIdTokenError, ExpiredIdTokenError
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a plaintext password (safely truncated for bcrypt)."""
    truncated = password.encode("utf-8")[:72].decode("utf-8", errors="ignore")
    return pwd_context.hash(truncated)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against its hashed version."""
    truncated = plain_password.encode("utf-8")[:72].decode("utf-8", errors="ignore")
    return pwd_context.verify(truncated, hashed_password)

def create_access_token(data: dict, secret_key: str, algorithm: str) -> str:
    """Create a JWT access token."""
    return encode(data, secret_key, algorithm=algorithm)

def decode_access_token(token: str, secret_key: str, algorithms: list) -> dict:
    """Decode a JWT access token."""
    try:
        return decode(token, secret_key, algorithms=algorithms)
    except PyJWTError:
        return None

def is_token_valid(token: str, secret_key: str, algorithms: list) -> bool:
    """Check if a JWT token is valid."""
    try:
        decode(token, secret_key, algorithms=algorithms)
        return True
    except PyJWTError:
        return False


# For firebase

def verify_firebase_token(id_token: str) -> dict:
    """Verify a Firebase ID token."""
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except exceptions.FirebaseError:
        return None
    
