from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=True)
    middle_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    birthdate = Column(DateTime(timezone=True), nullable=True)
    address = Column(String, nullable=True)
    contact_number = Column(String, nullable=True)
    is_seller = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)

    shop_name = Column(String, unique=True, index=True, nullable=True)
    shop_address = Column(String, nullable=True)
    shop_contact_number = Column(String, nullable=True)
    business_permit = Column(String, nullable=True)
    rating = Column(Float, default=0.0)
    rating_count = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    products = relationship("Product", back_populates="seller", cascade="all, delete-orphan")
    notifications = relationship("UserNotification", back_populates="user", cascade="all, delete-orphan")