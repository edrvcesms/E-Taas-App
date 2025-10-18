from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter
from schemas.users import UserResponse
from schemas.category import CreateCategory
from db.database import get_db
from services.admin import update_user_role, add_product_category
from models.users import User
from dependencies.auth import current_user


router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/add-category")
def add_new_category(new_category:CreateCategory, db: Session = Depends(get_db), user: User = Depends(current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can add categories")
    
    return add_product_category(db, new_category)


@router.put("/users/{user_id}/role", response_model=UserResponse)
def update_user_as_seller(user_id: int, db: Session = Depends(get_db), user: User = Depends(current_user)):

    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can update user roles")

    return update_user_role(db, user_id)



