from sqlalchemy import MetaData, Column, ForeignKey, Integer, String, Float
from database import Base
from sqlalchemy.orm import relationship
import schemas
import enum


metadata = MetaData()

class Goods(Base):
    __tablename__ = "goods"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(255))
    category_id = Column(Integer, ForeignKey("categories.id"))
    brand_id = Column(Integer, ForeignKey("brands.id"))
    price = Column(Float)

    images = relationship("Image", back_populates="good")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True)
    good_id = Column(Integer, ForeignKey("goods.id"))
    path = Column(String(50), nullable=False)

    good = relationship("Goods", back_populates="images")

class Roles(enum.Enum):
        user = 0
        manager = 1
        admin = 2

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    hashed_password = Column(String(2048), nullable=False)
    role = Column(Integer, default=Roles.user.value)

def scopes_maker(user: schemas.User):
        if user.role == Roles.user.value:
            return ["GoodsRead", "BrandsRead", "CategoriesRead"]
        if user.role == Roles.manager.value:
            return ["GoodsRead", "GoodsUpdate", "GoodsDelete", "GoodsCreate", 
                     "BrandsRead", "BrandsUpdate", "BrandsDelete", "BrandsCreate", 
                     "CategoriesRead", "CategoriesUpdate", "CategoriesDelete", 
                     "CategoriesCreate"]
        if user.role == Roles.admin.value:
            return ["GoodsRead", "GoodsUpdate", "GoodsDelete", "GoodsCreate", 
                     "BrandsRead", "BrandsUpdate", "BrandsDelete", "BrandsCreate", 
                     "CategoriesRead", "CategoriesUpdate", "CategpriesDelete", 
                     "CategoriesCreate", "UsersRead", "UsersUpdate", "UsersDelete", "UsersCreate"]
        
class Cart(Base):
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    good_id = Column(Integer, ForeignKey("goods.id"))
    count = Column(Integer, default=1)

