from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from datetime import datetime
from db.database import Base
from sqlalchemy.orm import relationship

class Service(Base):
    __tablename__ = 'services'

    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey('sellers.id'), nullable=False)
    service_name = Column(String, nullable=False)
    owner_name = Column(String, nullable=False)
    service_contact = Column(String, nullable=True)
    service_address = Column(String, nullable=True)
    description = Column(String, nullable=True)
    price_range = Column(String, nullable=True)
    fb_link = Column(String, nullable=True)
    banner_image = Column(String, nullable=True)
    is_available = Column(Boolean, default=True)
    ratings = Column(Float, default=0.00)
    created_at = Column(String, default=datetime.utcnow().isoformat())

    seller = relationship("Seller", back_populates="services")
    category = relationship("ServiceCategory", back_populates="service", cascade="all, delete-orphan")
    images = relationship("ServiceImage", back_populates="service", cascade="all, delete-orphan")
    inquiries = relationship("ServiceInquiry", back_populates="service")

class ServiceImage(Base):
    __tablename__ = 'service_images'

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey('services.id'), nullable=False)
    image_url = Column(String, nullable=False)

    service = relationship("Service", back_populates="images")