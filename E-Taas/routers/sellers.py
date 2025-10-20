from fastapi import HTTPException, APIRouter, status, Depends, Form, UploadFile, File
from sqlalchemy.orm import Session
from db.database import get_db
from typing import List, Dict
from services.notification import get_seller_notifications
from dependencies.auth import current_user
from schemas.products import ProductResponse, ProductUpdate
from services.products import get_all_products_by_seller, create_product, update_product, delete_product
from models.products import Product
from services.order import approve_order
from schemas.notification import SellerNotificationResponse
from models.users import User

router = APIRouter(prefix="/sellers", tags=["sellers"])

@router.get("/notifications", response_model=List[SellerNotificationResponse])
def seller_notifications(db: Session = Depends(get_db), user: User = Depends(current_user)):
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only logged-in users can view notifications")
    
    if not user.is_seller:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only sellers can view seller notifications")
    
    return get_seller_notifications(db, user.id)

@router.get("/products")
def get_seller_products(db: Session = Depends(get_db), user: User = Depends(current_user)):
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if not user.is_seller:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only sellers can view their products")
    
    return get_all_products_by_seller(db, user.id)

@router.post("/add-products", response_model = ProductResponse)
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

@router.put("/update-products", response_model=ProductResponse)
def update_product_by_id(product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db), user: User = Depends(current_user)):
    
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


@router.put("/approve-order/{order_id}")
async def approve_user_order(order_id: int, db: Session = Depends(get_db), user: User = Depends(current_user)):
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if not user.is_seller:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only sellers can approve orders")
    
    return await approve_order(db, order_id, "approved", user.id)


@router.delete("/delete-products/{id}")
def delete_product_by_id(product_id: int, db: Session = Depends(get_db), user: User = Depends(current_user)):
    if not user.is_seller:
        raise HTTPException(status_code=403, detail="Only sellers can delete products")
    
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    if product.seller_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only delete your own products")
    
    return delete_product(product_id, db)