from services.products import create_product, update_product, delete_product, get_all_product, get_product_by_id
from models.products import Product
from models.users import User
from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, Form
from typing import List
from fastapi import File
from db.database import get_db
from core.config import settings
from sqlalchemy.orm import Session
from schemas.products import ProductResponse, ProductUpdate
from dependencies.auth import current_user


router = APIRouter(prefix="/products", tags=["products"])

@router.get("/all")
def get_all_products(db: Session = Depends(get_db), user: User = Depends(current_user)):
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return get_all_product(db = db)

@router.get("/")
def get_product_with_id(product_id: int, db: Session = Depends(get_db), user: User = Depends(current_user)):
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return get_product_by_id(product_id=product_id, db=db)

    
