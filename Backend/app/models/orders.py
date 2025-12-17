from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from datetime import datetime
from db.database import Base
from sqlalchemy.orm import relationship

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    seller_id = Column(Integer, ForeignKey('sellers.id'), nullable=False)
    total_amount = Column(Float, nullable=False)
    shipping_address = Column(String, nullable=False)
    shipping_fee = Column(Float, nullable=False)
    payment_method = Column(String, nullable=False)
    order_reference = Column(String, unique=True, nullable=False)
    shipping_link = Column(String, nullable=True)
    status = Column(String, default="Pending", nullable=False)
    payment_status = Column(String, default="Unpaid", nullable=False)
    created_at = Column(String, default=datetime.utcnow().isoformat())
    shipped_at = Column(String, nullable=True)
    order_received_at = Column(String, nullable=True)

    user = relationship("User", back_populates="orders")
    seller = relationship("Seller", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    variant_id = Column(Integer, ForeignKey('product_variants.id'), nullable=True)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    created_at = Column(String, default=datetime.utcnow().isoformat())

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
    variant = relationship("ProductVariant", back_populates="order_items")


