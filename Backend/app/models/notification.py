from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from datetime import datetime
from app.db.database import Base
from sqlalchemy.orm import relationship

class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    seller_id = Column(Integer, ForeignKey('sellers.id'), nullable=True)
    role = Column(String, nullable=False)  # 'user' or 'seller'
    message = Column(String, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(String, default=datetime.utcnow().isoformat())

    user = relationship("User", back_populates="notifications")
    seller = relationship("Seller", back_populates="notifications")