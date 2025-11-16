from pydantic import BaseModel

class ProductCategoryBase(BaseModel):
    category_name: str

class ProductCategoryCreate(ProductCategoryBase):
    pass

class ServiceCategoryBase(BaseModel):
    name: str

class ServiceCategoryCreate(ServiceCategoryBase):
    pass