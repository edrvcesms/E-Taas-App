from fastapi import APIRouter, HTTPException, UploadFile, WebSocket, Depends, status, Form
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies.database import get_db
from dependencies.websocket import connection_manager
from services.chat import get_conversations_for_user, get_messages_for_conversation, add_new_message
from typing import List, Optional
from models.conversation import Conversation, Message
from schemas.chat import MessageCreate
from dependencies.auth import current_user

router = APIRouter()

@router.websocket("/ws/chat")
async def chat_websocket_endpoint(
    websocket: WebSocket,
    db: AsyncSession = Depends(get_db),
    user = Depends(current_user)
):
    user_id = user.id
    await connection_manager.connect(websocket, user_id)

    try:
        while True:
            data = await websocket.receive_text()
    except Exception:
        pass
    finally:
        connection_manager.disconnect(websocket, user_id)


@router.get("/conversations")
async def fetch_conversations(
    db: AsyncSession = Depends(get_db),
    user = Depends(current_user)
):
    return await get_conversations_for_user(db, user.id)

@router.get("/conversations/{conversation_id}/messages")
async def fetch_messages(
    conversation_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(current_user)
):
    return await get_messages_for_conversation(db, conversation_id)


@router.post("/messages", status_code=status.HTTP_201_CREATED)
async def post_message(
    message: str = Form(...),
    images: Optional[List[UploadFile]] = None,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(current_user)
):
    if message.sender not in ["user", "seller"]:
        raise HTTPException(status_code=400, detail="Invalid sender type.")
    
    if message.message is None and (not images or len(images) == 0):
        raise HTTPException(status_code=400, detail="Message must contain text or at least one image.")
    
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required.")
    return await add_new_message(db, message, images)