from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from models.notification import Notification
import logging
from dependencies.websocket import connection_manager

logger = logging.getLogger(__name__)


async def create_new_notification(db: AsyncSession, user_id: int, message: str) -> Notification:
    """Create a new notification for a user."""
    try:
        notification = Notification(user_id=user_id, message=message)
        db.add(notification)
        await db.commit()
        await db.refresh(notification)

        await connection_manager.send_message(message, user_id)

        logger.info(f"Notification created for user {user_id}: {message}")
        return notification
    
    except Exception as e:
        await db.rollback()
        logger.exception(f"Error creating notification for user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )