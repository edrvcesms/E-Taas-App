from fastapi import Depends, HTTPException, Header
from core.security import is_token_valid, decode_token
from core.firebase_config import verify_firebase_token
from core.config import settings
from models.users import User
from sqlalchemy.orm import Session
from db.database import get_db
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


bearer_scheme = HTTPBearer()

def current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
) -> User:
    token = credentials.credentials

    try:
        firebase_user = verify_firebase_token(token)
        if firebase_user:
            user = db.query(User).filter(User.email == firebase_user["email"]).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return user
    except Exception as e:
        print("Firebase error:", e)

    try:
        jwt_user = decode_token(token, settings.SECRET_KEY, [settings.ALGORITHM])
        if jwt_user and is_token_valid(token, settings.SECRET_KEY, [settings.ALGORITHM]):
            user = db.query(User).filter(User.id == jwt_user["user_id"]).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return user
    except Exception as e:
        print("JWT error:", e)

    raise HTTPException(status_code=401, detail="Invalid token")