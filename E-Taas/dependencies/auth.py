from fastapi import Depends, HTTPException, Header
from core.security import verify_firebase_token, is_token_valid, decode_access_token
from core.config import settings

def get_current_user(token: str = Header(...)):

    token = token.replace("Bearer ", "")

    try:
        firebase_user = verify_firebase_token(token)
        if firebase_user:
            return {"auth_provider": "firebase", "user": firebase_user}
        
        jwt_user = decode_access_token(token, settings.SECRET_KEY, [settings.ALGORITHM])
        if jwt_user and is_token_valid(token, settings.SECRET_KEY, [settings.ALGORITHM]):
            return {"auth_provider": "jwt", "user": jwt_user}
        
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")