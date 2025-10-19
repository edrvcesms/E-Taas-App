from sqlalchemy.orm import Session, joinedload
from models.cart import CartItem
from sqlalchemy.exc import SQLAlchemyError
from models.order import Order, OrderDetail
from schemas.order import OrderCreate
from models.users import User
from fastapi import HTTPException, status
from models.notification import UserNotification, SellerNotification
from routers.notification import manager

async def checkout_order(db: Session, user_id: int, order_data: OrderCreate) -> Order:
    selected_items = db.query(CartItem).filter(CartItem.id.in_(order_data.selected_items)).all()

    if not selected_items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No items selected")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    new_order = Order(
        user_id=user_id,
        total_amount=0,
        delivery_address=order_data.delivery_address,
        payment_method=order_data.payment_method,
        contact_number=order_data.contact_number
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    total_amount = 0
    order_details = []

    for item in selected_items:
        if item.cart.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot order items from another user's cart")

        product = item.product
        if product.stock < item.quantity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Not enough stock for product {product.name}")

        total_price = product.price * item.quantity
        total_amount += total_price

        order_detail = OrderDetail(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=product.price,
            total_price=total_price
        )
        order_details.append(order_detail)

        product.stock -= item.quantity
        db.delete(item)

    new_order.total_amount = total_amount
    db.add_all(order_details)
    db.commit()
    db.refresh(new_order)

    seller_ids = {item.product.seller_id for item in selected_items}
    for sid in seller_ids:
        message = f"{user.username} placed an order (Order ID: {new_order.id}) totaling {total_amount} PHP"
        db_notification = SellerNotification(user_id=sid, message=message)
        db.add(db_notification)
        db.commit()
        db.refresh(db_notification)
        await manager.send_personal_message(message, sid)

    return new_order
    
def get_order_by_id(db: Session, order_id: int, user_id: int) -> Order:
    order = db.query(Order).options(joinedload(Order.details)).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    if order.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to view this order")

    return order

def get_orders_by_user(db: Session, user_id: int) -> list[Order]:
    orders = db.query(Order).options(joinedload(Order.details)).filter(Order.user_id == user_id).all()
    return orders

def cancel_order(db: Session, order_id: int, status: str) -> Order:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    order.order_status = status
    db.commit()
    db.refresh(order)
    return order