from fastapi import APIRouter, Depends, HTTPException
from dependencies.auth import current_user
from sqlalchemy.orm import Session
from db.database import get_db
from models import User

router = APIRouter(prefix="/users", tags=["users"])

router.get("/")
def read_users(db: Session = Depends(get_db), user: dict = Depends(current_user)):
    """Get a list of all users. Requires authentication."""
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    users = db.query(User).all()
    return users