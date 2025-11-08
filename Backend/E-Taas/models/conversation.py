from sqlalchemy import Column, Integer, ForeignKey, String , Boolean
from db.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class Conversation(Base):
    __tablename__ = 'conversations'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    seller_id = Column(Integer, ForeignKey('sellers.id'), nullable=False)
    started_at = Column(String, default=datetime.utcnow().isoformat())

    user = relationship("User", back_populates="conversations")
    seller = relationship("Seller", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")



class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey('conversations.id'), nullable=False)
    sender = Column(String, nullable=False)  # 'user' or 'seller'
    message = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
    timestamp = Column(String, default=datetime.utcnow().isoformat())
    is_read = Column(Boolean, default=False)

    conversation = relationship("Conversation", back_populates="messages")
    images = relationship("MessageImage", back_populates="message", cascade="all, delete-orphan")

class MessageImage(Base):
    __tablename__ = 'message_images'

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey('messages.id'), nullable=False)
    image_url = Column(String, nullable=False)

    message = relationship("Message", back_populates="images")