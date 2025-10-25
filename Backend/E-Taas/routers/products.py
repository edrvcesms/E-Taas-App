from fastapi import HTTPException, status, APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from services.products import create_new_product
from schemas.product import ProductCreate, ProductBase, ProductResponse
from dependencies.auth import current_user
from dependencies.database import get_db
from models.users import User

router = APIRouter(
    prefix="/products",
    tags=["products"]
)


@router.post("/add-product", response_model=ProductResponse)
async def add_product(
    request: Request,
    product_data: ProductCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_user)
):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    
    if not user.is_seller:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only sellers can add products")
    
    return await create_new_product(db, product_data, user.id)

