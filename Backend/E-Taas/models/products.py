from datetime import datetime
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from db.database import Base

class Product(Base):
    __tablename__ = "products"


    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    base_price = Column(Numeric(10, 2), nullable=False)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    seller = relationship("User", back_populates="products")
    images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")
    variant_categories = relationship("VariantCategory", back_populates="product", cascade="all, delete-orphan")
    variants = relationship("Variant", back_populates="product", cascade="all, delete-orphan")
    category = relationship("Category", back_populates="products")

class VariantCategory(Base):
    __tablename__ = "variant_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    name = Column(String, nullable=False) # size, color, etc.
    values = Column(String, nullable=False) # Red, Blue, Green or S, M, L

    product = relationship("Product", back_populates="variant_categories")

class Variant(Base):
    __tablename__ = "variants"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    variant_combination = Column(String, nullable=False) # e.g., "Red-L", "Blue-M"
    price = Column(Numeric(10, 2), nullable=False)
    stock_quantity = Column(Integer, nullable=False, default=0)

    product = relationship("Product", back_populates="variants")
    images = relationship("VariantImage", back_populates="variant", cascade="all, delete-orphan")

class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    image_url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    product = relationship("Product", back_populates="images")

class VariantImage(Base):
    __tablename__ = "variant_images"

    id = Column(Integer, primary_key=True, index=True)
    variant_id = Column(Integer, ForeignKey("variants.id"), nullable=False)
    image_url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    variant = relationship("Variant", back_populates="images")
