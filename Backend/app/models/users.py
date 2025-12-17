from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from db.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    middle_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    address = Column(String, nullable=True)
    contact_number = Column(String, nullable=True)
    is_seller = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)

    seller = relationship("Seller", back_populates="user", uselist=False, cascade="all, delete-orphan")
    service_inquiries = relationship("ServiceInquiry", back_populates="user")
    orders = relationship("Order", back_populates="user")
    cart = relationship("Cart", back_populates="user", uselist=False, cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user")
    sent_conversations = relationship("Conversation", foreign_keys="[Conversation.sender_id]", back_populates="sender")
    received_conversations = relationship("Conversation", foreign_keys="Conversation.receiver_id", back_populates="receiver")

