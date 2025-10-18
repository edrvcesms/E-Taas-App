from pydantic import BaseModel

class CreateCategory(BaseModel):
    category_name: str

    class Config:
        orm_mode = True