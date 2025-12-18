from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime

class Conversation(Base):
    __tablename__ = 'conversations'

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    receiver_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow)

    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_conversations")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey('conversations.id'), nullable=False)
    sender_id = Column(Integer, nullable=False)
    sender_type = Column(String, nullable=False)  # 'user' or 'seller'
    message = Column(String, nullable=True) 
    timestamp = Column(DateTime, default=datetime.utcnow)
    is_read = Column(Boolean, default=False)

    conversation = relationship("Conversation", back_populates="messages")
    images = relationship("MessageImage", back_populates="message", cascade="all, delete-orphan")


class MessageImage(Base):
    __tablename__ = 'message_images'

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey('messages.id'), nullable=False)
    image_url = Column(String, nullable=False)

    message = relationship("Message", back_populates="images")
