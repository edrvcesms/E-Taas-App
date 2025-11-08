from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from db.database import Base
from sqlalchemy.orm import relationship

class ServiceInquiry(Base):
    __tablename__ = 'service_inquiries'

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey('services.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    seller_id = Column(Integer, ForeignKey('sellers.id'), nullable=False)
    contact_number = Column(String, nullable=False)
    message = Column(String, nullable=True)
    email = Column(String, nullable=False)

    service = relationship("Service", back_populates="inquiries")
    user = relationship("User", back_populates="service_inquiries")
    seller = relationship("Seller", back_populates="service_inquiries")