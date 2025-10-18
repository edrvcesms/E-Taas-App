
from schemas.category import CreateCategory
from models.category import Category
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.users import User


def update_user_role(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    user.is_seller = True
    db.commit()
    db.refresh(user)
    return user


def add_product_category(db: Session, create_category: CreateCategory):
    category = db.query(Category).filter(Category.name == create_category.category_name.lower()).first()

    if category:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Category already exists")
    
    new_category = Category(name=create_category.category_name.lower())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category