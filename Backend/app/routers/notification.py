from fastapi import APIRouter, status, WebSocket, WebSocketDisconnect
from app.dependencies.auth import decode_token
from app.core.config import settings
from app.dependencies.websocket import notification_manager
from asyncio import create_task
import json
from app.utils.logger import logger

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    heartbeat_task = None 
    user_id = None

    try:
        token = websocket.cookies.get("access_token")
        print("Access token retrieved from cookies:", token)

        if not token:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        payload = decode_token(token, settings.SECRET_KEY, [settings.ALGORITHM])
        user_id = payload.get("user_id")
        print ("Decoded user ID from token:", user_id)

        if not user_id:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        heartbeat_task = create_task(notification_manager.heartbeat(websocket))

        await notification_manager.connect(websocket, user_id)
        logger.info(f"User {user_id} connected to notifications websocket.")

        while True:
            try:
                data = await websocket.receive_text()
                message = json.loads(data)
                await notification_manager.send_message(message, user_id)
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
        notification_manager.disconnect(websocket, user_id)
