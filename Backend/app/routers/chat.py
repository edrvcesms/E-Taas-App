from fastapi import APIRouter, HTTPException, Query, UploadFile, WebSocket, Depends, status, Form, WebSocketDisconnect
from app.models.users import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.database import get_db
from app.services.chat import get_conversations_for_user, get_messages_for_conversation, send_new_message
from typing import List, Optional
from app.schemas.chat import MessageCreate
from app.dependencies.websocket import chat_manager
from app.dependencies.auth import current_user
from asyncio import create_task


router = APIRouter()


@router.get("/conversations", status_code=status.HTTP_200_OK)
async def fetch_conversations(
    db: AsyncSession = Depends(get_db),
    user = Depends(current_user)
):
    return await get_conversations_for_user(db, user.id)

@router.get("/conversations/{conversation_id}/messages", status_code=status.HTTP_200_OK)
async def fetch_messages(
    conversation_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(current_user)
):
    return await get_messages_for_conversation(db, conversation_id)


@router.post("/send-message", status_code=status.HTTP_201_CREATED)
async def post_message(
    message: str = Form(...),
    images: Optional[List[UploadFile]] = None,
    conversation_id: Optional[int] = Form(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user)
):
    
    parsed_data = MessageCreate.parse_raw(message)

    return await send_new_message(db, parsed_data, current_user.id, images, conversation_id)