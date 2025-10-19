from fastapi import APIRouter, WebSocket, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies.auth import current_user
from db.database import get_db
from models.users import User
from schemas.notification import UserNotificationResponse, SellerNotificationResponse
from services.notification import get_user_notifications, get_seller_notifications
from typing import List, Dict

router = APIRouter(prefix="/notification", tags=["notification"])

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)

    def disconnect(self, websocket: WebSocket, user_id: int):
        if user_id in self.active_connections:
            self.active_connections[user_id].remove(websocket)

    async def send_personal_message(self, message: str, user_id: int):
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                await connection.send_text(message)

manager = ConnectionManager()

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        manager.disconnect(websocket, user_id)

@router.get("/user-notifications", response_model=List[UserNotificationResponse])
def user_notifications(db: Session = Depends(get_db), user: User = Depends(current_user)):
    if not user:
        raise HTTPException(status_code=403, detail="Only logged-in users can view notifications")
    
    return get_user_notifications(db, user.id)

@router.get("/seller-notifications", response_model=List[SellerNotificationResponse])
def seller_notifications(db: Session = Depends(get_db), user: User = Depends(current_user)):
    if not user.is_seller:
        raise HTTPException(status_code=403, detail="Only sellers can view seller notifications")
    return get_seller_notifications(db, user.id)