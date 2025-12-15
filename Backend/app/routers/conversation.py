from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status
from asyncio import create_task
from core.security import decode_token
from core.config import settings
from dependencies.websocket import chat_manager
from utils.logger import logger
import json



router = APIRouter()

@router.websocket("/ws")
async def chat_websocket_endpoint(websocket: WebSocket):
    heartbeat_task = None 

    try:
        token = websocket.cookies.get("access_token")
        print("Access token retrieved from cookies:", token)

        if not token:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        payload = decode_token(token, settings.SECRET_KEY, [settings.ALGORITHM])
        user_id = payload.get("user_id")

        if not user_id:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        heartbeat_task = create_task(chat_manager.heartbeat(websocket))

        await chat_manager.connect(websocket, user_id)
        logger.info(f"User {user_id} connected to notifications websocket.")

        while True:
            try:
                data = await websocket.receive_text()
                message = json.loads(data)
                await chat_manager.send_message(message, user_id)
            except WebSocketDisconnect:
                logger.info(f"User {user_id} disconnected.")
                break
            except Exception as e:
                logger.error(f"Error in websocket communication: {e}")
                break

    except Exception as e:
        logger.error(f"WebSocket connection error: {e}")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)

    finally:
        if heartbeat_task:
            heartbeat_task.cancel()
        chat_manager.disconnect(websocket, user_id)