from fastapi import APIRouter, HTTPException, Request, status, Depends, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.database import get_db
from app.services.service import get_all_services, upload_service_image, get_service_by_id, create_service
from app.schemas.service import ServiceCreate
from app.dependencies.auth import current_user
from app.models.users import User
from app.dependencies.limiter import limiter

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

@router.post("/add-service-images/{service_id}", status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
async def upload_images_to_service(
    request: Request,
    service_id: int,
    files: list[UploadFile] = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user)
):
    """Upload images to a specific service."""
    if not current_user or not current_user.is_seller:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only sellers can upload service images."
        )
    
    return await upload_service_image(db, service_id, files)

@router.post("/add-service", status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def create_new_service(
    request: Request,
    service_data: ServiceCreate,
    current_user: User = Depends(current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new service. Requires authentication."""
    if not current_user.id or not current_user.is_seller:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create a service"
        )
    

    service = await create_service(service_data, current_user.seller.id, db)
        
    return service