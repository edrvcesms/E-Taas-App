from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.cart import CartResponse, CartItemBase, CartItemUpdate
from services.cart import get_or_create_cart, add_item_to_cart, update_cart_item_quantity, remove_item_from_cart
from db.database import get_db
from dependencies.auth import current_user
from models.users import User

router = APIRouter(prefix="/cart", tags=["cart"])

@router.get("/", response_model=CartResponse)
def get_user_cart(db: Session = Depends(get_db), user: User = Depends(current_user)):
    
    return get_or_create_cart(db, user.id)

@router.post("/items", response_model=CartResponse)
def add_to_cart(item: CartItemBase, db: Session = Depends(get_db), user: User = Depends(current_user)):
    
    return add_item_to_cart(db, user.id, item.product_id, item.quantity)

@router.put("/items/{product_id}", response_model=CartResponse)
def update_cart_item(product_id: int, item: CartItemUpdate, db: Session = Depends(get_db), user: User = Depends(current_user)):
    
    if item.quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quantity must be positive. To remove an item, use the DELETE endpoint.",
        )
    return update_cart_item_quantity(db, user.id, product_id, item.quantity)

@router.delete("/clear-all", status_code=status.HTTP_204_NO_CONTENT)
def clear_cart(db: Session = Depends(get_db), user: User = Depends(current_user)):
    
    cart = get_or_create_cart(db, user.id)
    for item in cart.items:
        db.delete(item)
    db.commit()
    return None

@router.delete("/items/{product_id}", response_model=CartResponse)
def remove_from_cart(product_id: int, db: Session = Depends(get_db), user: User = Depends(current_user)):
    
    return remove_item_from_cart(db, user.id, product_id)


