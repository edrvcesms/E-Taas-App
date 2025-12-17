from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from db.database import Base
from sqlalchemy.orm import relationship

class Seller(Base):
    __tablename__ = 'sellers'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)
    business_name = Column(String, nullable=False)
    business_address = Column(String, nullable=True)
    business_contact = Column(String, nullable=True)
    display_name = Column(String, nullable=True)
    owner_address = Column(String, nullable=True)
    is_verified = Column(Boolean, default=False)
    is_seller_mode = Column(Boolean, default=False)
    followers = Column(Integer, default=0)
    ratings = Column(Float, default=0.00)

    user = relationship("User", back_populates="seller")
    products = relationship("Product", back_populates="seller", cascade="all, delete-orphan")
    services = relationship("Service", back_populates="seller", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="seller")
    service_inquiries = relationship("ServiceInquiry", back_populates="seller")
    notifications = relationship("Notification", back_populates="seller")