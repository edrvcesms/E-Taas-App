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

@router.post("/add", response_model = ProductResponse)
def add_product(
    product_name: str = Form(),
    price: float = Form(),
    description: str = Form(None),
    stock: int = Form(0),
    category_id: int = Form(),
    images: List[UploadFile] = File(),
    db: Session = Depends(get_db),
    user: User = Depends(current_user)
    ):

    if not user.is_seller:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only sellers can add products")
    
    product_data = {
        "product_name": product_name,
        "price": price,
        "description": description,
        "stock": stock,
        "category_id": category_id,
        "seller_id": user.id, 
    }

    return create_product(product_data, images, db)

@router.put("/update", response_model=ProductResponse)
def product_update(product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db), user: User = Depends(current_user)):
    
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    if not user.is_seller:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only sellers can update products")
    
    if product.seller_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only update your own products")
    
    update_product_data = product_update.dict(exclude_unset=True)

    updated_product = update_product(product_id, update_product_data, db)
    return updated_product

@router.delete("/delete/{id}")
def product_delete(product_id: int, db: Session = Depends(get_db), user: User = Depends(current_user)):
    if not user.is_seller:
        raise HTTPException(status_code=403, detail="Only sellers can delete products")
    
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    return delete_product(product_id, db)
    
