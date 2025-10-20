from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime, func
from db.database import Base
from sqlalchemy.orm import relationship

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total_amount = Column(Float)
    order_status = Column(String, default="pending")
    delivery_address = Column(String)
    payment_method = Column(String)
    contact_number = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    seller = relationship("User", back_populates="order_seller", foreign_keys=[seller_id])
    user = relationship("User", back_populates="orders", foreign_keys=[user_id])
    details = relationship("OrderDetail", back_populates="orders")

class OrderDetail(Base):
    __tablename__ = "order_details"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    price = Column(Float)
    total_price = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    orders = relationship("Order", back_populates="details")
    product = relationship("Product", back_populates="order_details")
