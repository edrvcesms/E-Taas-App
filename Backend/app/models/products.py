from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Table
from datetime import datetime
from app.db.database import Base
from sqlalchemy.orm import relationship

variant_attribute_values = Table(
    'variant_attribute_values',
    Base.metadata,
    Column('variant_id', Integer, ForeignKey('product_variants.id'), primary_key=True),
    Column('attribute_id', Integer, ForeignKey('variant_attributes.id'), primary_key=True)
)
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey('sellers.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('product_categories.id'), nullable=False)
    product_name = Column(String, nullable=False)
    base_price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    description = Column(String, nullable=True)
    has_variants = Column(Boolean, default=False)
    created_at = Column(String, default=datetime.utcnow().isoformat())

    seller = relationship("Seller", back_populates="products")
    images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")
    variants = relationship("ProductVariant", back_populates="product", cascade="all, delete-orphan")
    variant_categories = relationship("VariantCategory", back_populates="product", cascade="all, delete-orphan")
    category = relationship("ProductCategory", back_populates="product")
    cart_items = relationship("CartItem", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")

class ProductImage(Base):
    __tablename__ = 'product_images'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    image_url = Column(String, nullable=False)

    product = relationship("Product", back_populates="images")

class ProductVariant(Base):
    __tablename__ = 'product_variants'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    variant_name = Column(String, nullable=False)
    stock = Column(Integer, default=0)
    price = Column(Float, nullable=False)
    image_url = Column(String, nullable=False)

    product = relationship("Product", back_populates="variants")
    order_items = relationship("OrderItem", back_populates="variant")
    attributes = relationship("VariantAttribute", secondary='variant_attribute_values', back_populates="product_variants")
    cart_items = relationship("CartItem", back_populates="variant")

class VariantCategory(Base):
    __tablename__ = 'variant_categories'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    category_name = Column(String, nullable=False)

    product = relationship("Product", back_populates="variant_categories")
    attributes = relationship("VariantAttribute", back_populates="category", cascade="all, delete-orphan")

class VariantAttribute(Base):
    __tablename__ = 'variant_attributes'

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey('variant_categories.id'), nullable=False)
    value = Column(String, nullable=False)

    category = relationship("VariantCategory", back_populates="attributes")
    product_variants = relationship("ProductVariant", secondary='variant_attribute_values', back_populates="attributes")
