from fastapi import APIRouter, Depends, HTTPException, status
from dependencies.auth import current_user
from schemas.users import UserResponse, UserUpdate
from sqlalchemy.orm import Session
from services.users import get_user_details, update_user_details, delete_user_account
from db.database import get_db
from models import User

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/profile", response_model=UserResponse)
def get_user_profile(db: Session = Depends(get_db), user: User = Depends(current_user)):
    db_user = db.query(User).filter(User.id == user.id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/update-profile", response_model=UserResponse)
def update_user(update_details: UserUpdate, db: Session = Depends(get_db), user: User = Depends(current_user)):
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    update_data = update_details.dict(exclude_unset=True)

    updated_user = update_user_details(user.id, update_data, db)

    return updated_user

@router.delete("/delete-account")
def delete_user(db: Session = Depends(get_db), user: User = Depends(current_user)):
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return delete_user_account(user.id, db)


