from sqlalchemy import MetaData, Column, ForeignKey, Integer, String
from database import Base
from sqlalchemy.orm import relationship


metadata = MetaData()

class Goods(Base):
    __tablename__ = "goods"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(255))
    category_id = Column(Integer, ForeignKey("categories.id"))
    brand_id = Column(Integer, ForeignKey("brands.id"))

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



