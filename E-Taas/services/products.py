from core.cloudinary_config import cloudinary
import cloudinary.uploader
from models import Product
from sqlalchemy.orm import Session
from datetime import datetime
from models.products import ProductImages


def create_product(product: dict, images: list, db: Session):
    new_product = Product(
        product_name=product["product_name"],
        price=product["price"],
        description=product.get("description"),
        stock=product.get("stock", 0),
        category_id=product["category_id"],
        seller_id=product["seller_id"],
        created_at=datetime.utcnow()
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    for image in images:
        upload_result = cloudinary.uploader.upload(image.file)
        print("Cloudinary Config:", cloudinary.config())
        image_url = upload_result["secure_url"]
        db.add(ProductImages(product_id=new_product.id, image_url=image_url))

    db.commit()
    db.refresh(new_product)
    return new_product


def get_all_product(db: Session, limit = 100):
    return db.query(Product).limit(limit=limit).all()


def get_product_by_id(product_id: int, db: Session):
    return db.query(Product).filter(Product.id == product_id).first()

def get_all_products_by_seller(db: Session, seller_id: int):
    return db.query(Product).filter(Product.seller_id == seller_id).all()


def update_product(product_id: int, update_product: dict, db: Session):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None
    for key, value in update_product.items():
        setattr(product, key, value)
    product.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(product)
    return product

def delete_product(product_id: int, db: Session):
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return None
        db.delete(product)
        db.commit()
        return {"Success": "Deletion of product successful"}
    except:
        return {"Error", "Something went wrong on deletion"}
    
