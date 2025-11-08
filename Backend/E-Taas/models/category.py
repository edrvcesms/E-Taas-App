from sqlalchemy import Column, Integer, String, ForeignKey
from db.database import Base
from sqlalchemy.orm import relationship

class ProductCategory(Base):
    __tablename__ = 'product_categories'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    category_name = Column(String, nullable=False)

    product = relationship("Product", back_populates="category")

class ServiceCategory(Base):
    __tablename__ = 'service_categories'

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey('services.id'), nullable=False)
    category_name = Column(String, nullable=False)

    service = relationship("Service", back_populates="category")