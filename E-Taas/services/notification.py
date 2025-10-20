from sqlalchemy.orm import Session
from models.notification import UserNotification, SellerNotification


def get_user_notifications(db: Session, user_id: int):
    user_notifications = db.query(UserNotification).filter(UserNotification.user_id == user_id).all()
    return user_notifications

def get_seller_notifications(db: Session, seller_id: int):
    seller_notifications = db.query(SellerNotification).filter(SellerNotification.seller_id == seller_id).all()
    return seller_notifications