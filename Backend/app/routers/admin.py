from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.database import get_db
from app.dependencies.auth import current_user
from app.services.admin import add_product_category, add_service_category, approve_seller, get_sellers_applications, get_all_sellers, get_all_users
from app.services.auth import create_admin_user
from app.schemas.users import UserBase
from app.schemas.auth import AdminRegister
from app.schemas.category import ProductCategoryCreate, ServiceCategoryCreate
from app.models.users import User
from app.dependencies.limiter import limiter

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
async def register_admin(
    request: Request,
    admin_data: AdminRegister,
    db: AsyncSession = Depends(get_db),
):
    """Register a new admin. Only run once by the deverloper."""
    return await create_admin_user(db, admin_data)
  

@router.post("/add-product-category", status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def create_product_category(
    request: Request,
    category: ProductCategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user)
):
    """Add a new product category. Admin only."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform this action"
        )
    return await add_product_category(db, category)

@router.post("/add-service-category", status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def create_service_category(
    request: Request,
    category: ServiceCategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user)
):
    """Add a new service category. Admin only."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform this action"
        )
    return await add_service_category(db, category)


@router.get("/seller-applications", status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")
async def manage_sellers_application(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user)
):
    """Get all seller applications. Admin only."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform this action"
        )
    return await get_sellers_applications(db)



@router.get("/sellers", status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")
async def get_sellers(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user)
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform this action"
        )
    return await get_all_sellers(db)

@router.get("/users", status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")
async def get_users(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user)
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform this action"
        )
    
    return await get_all_users(db)

@router.put("/verify-seller", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
async def verify_seller(
    request: Request,
    seller_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user)
):
    """Approve a seller. Admin only."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform this action"
        )
    return await approve_seller(db, seller_id)