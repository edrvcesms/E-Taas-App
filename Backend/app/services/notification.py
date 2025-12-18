from fastapi import HTTPException, status
from sqlalchemy import or_, select
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.notification import Notification
from app.dependencies.websocket import notification_manager
from app.models.users import User
from app.utils.logger import logger


async def create_new_notification(db: AsyncSession, target_id: int, message: str, role: str) -> Notification:
    """Create a new notification for a user."""
    try:
        if role == "seller":
            notification = Notification(
                seller_id=target_id,
                message=message,
                role=role
            )
        else:
            notification = Notification(
                user_id=target_id,
                message=message,
                role=role
            )
        db.add(notification)
        await db.commit()
        await db.refresh(notification)

        notification_data = {
            "id": notification.id,
            "message": notification.message,
            "is_read": notification.is_read,
            "created_at": str(notification.created_at),
            "role": notification.role
        }

        await notification_manager.send_message(notification_data, target_id)

        logger.info(f"Notification created for user {target_id}: {message}")
        return notification
    
    except HTTPException:
        raise
    
    except Exception as e:
        await db.rollback()
        logger.exception(f"Error creating notification for user {target_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    
async def get_notifications_for_user(db: AsyncSession, user_id: int, seller_id: int | None = None) -> List[Notification]:
    try:
        filters = [
            Notification.user_id == user_id
        ]

        if seller_id:
            filters.append(Notification.seller_id == seller_id)

        result = await db.execute(
            select(Notification)
            .where(or_(*filters))
            .order_by(Notification.created_at.desc())
        )

        return result.scalars().all()
    
    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error retrieving notifications for user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    
async def mark_notification_as_read(db: AsyncSession, notification_id: int, user_id: int) -> Notification:
    try:
        result = await db.execute(select(Notification).where(Notification.id == notification_id, Notification.user_id == user_id))
        notification = result.scalar_one_or_none()

        if not notification:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found."
            )

        notification.is_read = True
        await db.commit()
        await db.refresh(notification)

        logger.info(f"Marked notification {notification_id} as read for user {user_id}")
        return notification

    except HTTPException:
        raise

    except Exception as e:
        await db.rollback()
        logger.error(f"Error marking notification {notification_id} as read for user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    
async def mark_all_notifications_as_read(db: AsyncSession, user_id: int) -> int:
    try:
        result = await db.execute(select(Notification).where(Notification.user_id == user_id, Notification.is_read == False))
        notifications = result.scalars().all()

        if not notifications:
            return 0

        for notification in notifications:
            notification.is_read = True

        await db.commit()
        logger.info(f"Marked all notifications as read for user {user_id}")
        return len(notifications)

    except HTTPException:
        raise

    except Exception as e:
        await db.rollback()
        logger.error(f"Error marking all notifications as read for user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        ) from e
    
