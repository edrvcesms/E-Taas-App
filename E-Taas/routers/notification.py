from fastapi import APIRouter, Depends, status, Request, WebSocket, WebSocketDisconnect, Query
from dependencies.auth import decode_token
from core.config import settings
from dependencies.websocket import connection_manager
from asyncio import create_task

router = APIRouter(
    prefix="/notifications",
    tags=["notifications"]
)


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str = Query(...)):

    try:
        payload = decode_token(token, settings.SECRET_KEY, [settings.ALGORITHM])
        user_id = payload["user_id"]
    except Exception:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    try:
        await connection_manager.connect(websocket, user_id)
        heartbeat_task = create_task(connection_manager.heartbeat(websocket))

        while True:
            try:
                data = await websocket.receive_text()
            except WebSocketDisconnect:
                break
            except Exception as e:
                break

    finally:
        heartbeat_task.cancel()
        connection_manager.disconnect(websocket, user_id)