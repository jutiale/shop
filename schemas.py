from pydantic import BaseModel
from typing import Union


class GoodBase(BaseModel):
    name: str
    description: Union[str, None] = None    
    category_id: int
    brand_id: int


class GoodRead(GoodBase):
    pass

class GoodCreate(GoodBase):
    pass

class GoodUpdate(GoodBase):
    pass

class Good(GoodBase):
    id: int
    class Config:
        orm_mode = True


class CategoryBase(BaseModel):
    # id : int
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    class Config:
        orm_mode = True


class BrandBase(BaseModel):
    name: str

class BrandRead(BrandBase):
    pass

class BrandCreate(BrandBase):
    pass 

class BrandUpdate(BrandBase):
    pass

class Brand(BrandBase):
    id: int
    class Config:
        orm_mode = True

class ImageBase(BaseModel):
    path: str
    good_id: int

class ImageCreate(ImageBase):
    pass

class ImageRead(ImageBase):
    pass

class Image(ImageBase):
    id: int
    class Config:
        orm_mode = True