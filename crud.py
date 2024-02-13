from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import models, schemas
from fastapi.responses import FileResponse
import os
from fastapi import UploadFile
from fastapi import HTTPException


def get_good(db: Session, good_id: int):
    return db.query(models.Goods).filter(models.Goods.id == good_id).first()

def get_goods(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Goods).offset(skip).limit(limit).all()


def create_good(db: Session, good: schemas.GoodCreate):
    db_good = models.Goods(name=good.name, description=good.description, 
                           category_id=good.category_id, brand_id=good.brand_id)
    db.add(db_good)
    db.commit()
    db.refresh(db_good)
    return db_good

def delete_good(db: Session, db_good: schemas.Good):
    db.delete(db_good)
    db.commit()
    return {"ok": True}

def update_good(db: Session, good: schemas.GoodUpdate, db_good: schemas.Good):
    good_data = good.model_dump(exclude_unset=True)
    for key, value in good_data.items():
        setattr(db_good, key, value)
    db.add(db_good)
    db.commit()
    db.refresh(db_good)
    return db_good

def get_category(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Category).offset(skip).limit(limit).all()


def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db: Session, db_category: schemas.Category):
    try:
        db.delete(db_category)
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Cannot delete the category")
    return {"ok": True}

def update_category(db: Session, category: schemas.CategoryUpdate, db_category: schemas.Category):
    category_data = category.model_dump(exclude_unset=True)
    for key, value in category_data.items():
        setattr(db_category, key, value)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_brand(db: Session, brand_id: int):
    return db.query(models.Brand).filter(models.Brand.id == brand_id).first()

def get_brands(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Brand).offset(skip).limit(limit).all()


def create_brand(db: Session, brand: schemas.BrandCreate):
    db_brand = models.Brand(name=brand.name)
    db.add(db_brand)
    db.commit()
    db.refresh(db_brand)
    return db_brand

def delete_brand(db: Session, db_brand: schemas.Brand):
    try:
        db.delete(db_brand)
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Cannot delete the brand")
    return {"ok": True}

def update_brand(db: Session, brand: schemas.BrandUpdate, db_brand: schemas.Brand):
    brand_data = brand.model_dump(exclude_unset=True)
    for key, value in brand_data.items():
        setattr(db_brand, key, value)
    db.add(db_brand)
    db.commit()
    db.refresh(db_brand)
    return db_brand


def upload_image(file: UploadFile):
    file_location = f"images/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    return file_location

def create_upload_image(db: Session, good_id: int, path: str):
    db_image = models.Image(path=path, good_id=good_id)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

def get_image(db: Session, image_id: int):
    return db.query(models.Image).filter(models.Image.id == image_id).first()

def delete_image(db: Session, db_image: schemas.Image):
    db.delete(db_image)
    db.commit()
    os.unlink(db_image.path)
    return {"ok": True}
