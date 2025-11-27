from fastapi import APIRouter, HTTPException, Request, status, Depends, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies.database import get_db
from services.service import get_all_services, upload_service_image, get_service_by_id, create_service
from schemas.service import ServiceCreate
from dependencies.auth import current_user
from models.users import User
from dependencies.limiter import limiter

router = APIRouter()

@router.get("/")
@limiter.limit("30/minute")
async def get_services(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Retrieve all services."""
    return await get_all_services(db)

@router.get("/{service_id}")
@limiter.limit("10/minute")
async def view_service_details(
    request: Request,
    service_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Retrieve service details by service ID."""
    return await get_service_by_id(service_id, db)

@router.post("/create-service", status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def create_new_service(
    request: Request,
    service_data: str = Form(...),
    service_images: list[UploadFile] = File(...),
    current_user: User = Depends(current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new service. Requires authentication."""
    if not current_user.id or not current_user.is_seller:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create a service"
        )
    
    parsed_service_data = ServiceCreate.parse_raw(service_data)

    service = await create_service(parsed_service_data, current_user.sellers[0].id, db)
    
    if service_images:
        await upload_service_image(db, service.id, service_images)
        
    return service