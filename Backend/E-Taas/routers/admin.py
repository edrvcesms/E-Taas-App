from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies.database import get_db
from dependencies.auth import current_user
from services.admin import add_new_category
from models.users import User
from dependencies.limiter import limiter

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

@router.post("/add-category", status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def create_category(
    request: Request,
    category_name: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user)
):
    """Add a new product category. Admin only."""

    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform this action"
        )

    return await add_new_category(db, category_name)