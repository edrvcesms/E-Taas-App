from fastapi import HTTPException, status, UploadFile
from dependencies.websocket import chat_manager
from sqlalchemy import or_, select
from sqlalchemy.orm import selectinload
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from models.conversation import Conversation, MessageImage, Message
from utils.logger import logger
from utils.cloudinary import upload_image_to_cloudinary
from schemas.chat import MessageCreate

async def get_conversations_for_user(db: AsyncSession, user_id: int) -> List[Conversation]:
    try:
        result = await db.execute(
            select(Conversation).where(
                or_(
                    Conversation.sender_id == user_id,
                    Conversation.receiver_id == user_id  
                )
            )
        )
        
        conversations = result.scalars().all()
        logger.info(f"Fetched {len(conversations)} conversations for user {user_id}")
        
        return conversations or []

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching conversations for user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch conversations for the user."
        ) from e
async def get_messages_for_conversation(db: AsyncSession, conversation_id: int) -> List[Message]:
    try:
        result = await db.execute(
            select(Message)
            .options(selectinload(Message.images))
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.timestamp.asc())
        )
        messages = result.scalars().all()
        logger.info(f"Fetched {len(messages)} messages for conversation {conversation_id}")
        if not messages:
            return []
        return messages
    
    except HTTPException:
        raise
    
    except Exception as e:
        logger.error(f"Error fetching messages for conversation {conversation_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch messages for the conversation."
        ) from e
    
async def create_a_conversation(db: AsyncSession, sender_id: int, receiver_id: int) -> Conversation:
    try:
        existing_result = await db.execute(
            select(Conversation).where(
                Conversation.sender_id == sender_id,
                Conversation.receiver_id == receiver_id
            )
        )
        existing_conversation = existing_result.scalar_one_or_none()
        if existing_conversation:
            logger.info(f"Conversation already exists between user {sender_id} and seller {receiver_id}")
            return existing_conversation

        new_conversation = Conversation(
            sender_id=sender_id,
            receiver_id=receiver_id
        )
        db.add(new_conversation)
        await db.commit()
        await db.refresh(new_conversation)

        logger.info(f"Created new conversation {new_conversation.id} between user {sender_id} and seller {receiver_id}")
        return new_conversation
    
    except HTTPException:
        raise
    
    except Exception as e:
        await db.rollback()
        logger.error(f"Error creating conversation between user {sender_id} and seller {receiver_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create conversation."
        ) from e
    
async def send_new_message(db: AsyncSession, message_data: MessageCreate, sender_id: int, images: Optional[List[UploadFile]] = None, conversation_id: Optional[int] = None) -> Message:
    try:
        result = await db.execute(select(Conversation).where(Conversation.id == conversation_id))
        conversation = result.scalar_one_or_none()
        if not conversation:
            conversation = await create_a_conversation(db, sender_id, message_data.receiver_id)
        
        new_message = Message(
            conversation_id=conversation.id,
            sender_id=sender_id,
            message=message_data.message,
            sender_type=message_data.sender_type
        )
        db.add(new_message)
        await db.commit()
        await db.refresh(new_message)

        if images:
            for image in images:
                image_url = await upload_image_to_cloudinary([image], folder="chat_images")
                for url in image_url:
                    message_image = MessageImage(
                        message_id=new_message.id,
                        image_url=url["secure_url"]
                    )
                    db.add(message_image)
                    await db.flush()
            await db.commit()   
        await db.refresh(new_message)

        result = await db.execute(
            select(Message)
            .options(selectinload(Message.images))
            .where(Message.id == new_message.id)
        )
        new_message = result.scalar_one_or_none()

        new_message_data = {
            "id": new_message.id,
            "conversation_id": new_message.conversation_id,
            "sender_id": new_message.sender_id,
            "message": new_message.message,
            "timestamp": str(new_message.timestamp),
            "sender_type": new_message.sender_type,
            "images": [image.image_url for image in new_message.images]
        }


        logger.info(f"Sent new message {new_message.id} in conversation {conversation.id}")
        await chat_manager.send_message(new_message_data, message_data.receiver_id)
        return new_message
    
    except HTTPException: 
        raise

    except Exception as e:
        await db.rollback()
        logger.error(f"Error sending message from sender {sender_id} in conversation {conversation_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send message."
        ) from e
    
