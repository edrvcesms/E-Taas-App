from fastapi import HTTPException, status, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.services import Service, ServiceImage
from app.schemas.service import ServiceCreate
from app.utils.cloudinary import upload_image_to_cloudinary

async def get_all_services(db: AsyncSession):
    try:
        result = await db.execute(select(Service))
        services = result.scalars().all()
        return services
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
async def upload_service_image(db: AsyncSession, service_id: int, files: list[UploadFile]):
    try:
        result = await db.execute(select(ServiceImage).where(ServiceImage.service_id == service_id))
        existing_images = result.scalars().all() or []

        if len(existing_images) + len(files) > 10:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot upload more than 10 images for a service."
            )

        uploaded_images = []
        for file in files:
            upload_result = await upload_image_to_cloudinary([file], folder="services_images")
            new_service_image = ServiceImage(
                service_id=service_id,
                image_url=upload_result[0]["secure_url"],
            )
            db.add(new_service_image)
            uploaded_images.append(new_service_image)

        await db.commit()
        return uploaded_images

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def get_service_by_id(service_id: int, db: AsyncSession):
    try:
        result = await db.execute(select(Service).where(Service.id == service_id))
        service = result.scalars().first()
        if not service:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
        return service
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
async def create_service(service_data: ServiceCreate, seller_id: int, db: AsyncSession):
    
    if not seller_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Seller ID is required to create a service")
    try:
        new_service = Service(
            seller_id=seller_id,
            category_id=service_data.category_id,
            service_name=service_data.service_name,
            owner_name=service_data.owner_name,
            service_contact=service_data.service_contact,
            service_address=service_data.service_address,
            description=service_data.description,
            price_range=service_data.price_range,
            fb_link=service_data.fb_link,
            is_available=service_data.is_available
        )
        db.add(new_service)
        await db.commit()
        await db.refresh(new_service)
        return new_service

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) 