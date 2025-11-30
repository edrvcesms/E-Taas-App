from fastapi import APIRouter, HTTPException, Query, WebSocket, WebSocketDisconnect, status
from sqlalchemy.ext.asyncio import AsyncSession
from asyncio import create_task
from core.security import decode_token
from core.config import settings
from dependencies.websocket import chat_manager



router = APIRouter()

@router.websocket("/ws/conversations")
async def chat_websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(...)
):
    try:
        payload = decode_token(token, settings.SECRET_KEY, [settings.ALGORITHM])
        user_id = payload["user_id"]
    except Exception:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    try:
        await chat_manager.connect(websocket, user_id)
        heartbeat_task = create_task(chat_manager.heartbeat(websocket))

        while True:
            try:
                data = await websocket.receive_text()
                await chat_manager.send_message(data, user_id)
            except WebSocketDisconnect:
                break
            except Exception as e:
                break

    finally:
        heartbeat_task.cancel()
        await chat_manager.disconnect(websocket, user_id)