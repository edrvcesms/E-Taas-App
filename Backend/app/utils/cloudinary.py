from app.core.cloudinary import cloudinary
from cloudinary.uploader import upload
from fastapi import UploadFile
from typing import List


async def upload_image_to_cloudinary(files: List[UploadFile], folder: str):
    results = []
    for file in files:
        contents = await file.read()
        if not contents:
            continue
        result = upload(
            contents,
            folder=folder
        )
        results.append({
            "secure_url": result["secure_url"],
            "public_id": result["public_id"]
        })
    return results

async def upload_single_image_to_cloudinary(file: UploadFile, folder: str):
    contents = await file.read()
    if not contents:
        raise ValueError("File is empty")
    result = cloudinary.uploader.upload(
        contents,
        folder=folder
    )
    return {
        "secure_url": result["secure_url"],
        "public_id": result["public_id"]
    }

async def delete_image_from_cloudinary(public_id: str):
    result = cloudinary.uploader.destroy(public_id)
    return result