from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, schemas
from database import SessionLocal, engine
from typing import List
from fastapi import FastAPI, File, UploadFile


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}
    

@app.get("/goods/", response_model=List[schemas.Good])  # Просмотр списка товаров
def read_goods(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    goods = crud.get_goods(db, skip=skip, limit=limit)
    return goods

@app.get("/goods/{good_id}", response_model=schemas.Good)  # Поиск по id 
def read_good(good_id: int, db: Session = Depends(get_db)):
    good = crud.get_good(db, good_id)
    return good
 
@app.post("/goods/", response_model=schemas.Good)  # Создание 
def create_good(good: schemas.GoodCreate, db: Session = Depends(get_db)):
    return crud.create_good(db, good)

@app.delete("/goods/{good_id}")  # Удаление 
def delete_good(good_id: int, db: Session = Depends(get_db)):
    db_good = crud.get_good(db, good_id)
    if not db_good:
        raise HTTPException(status_code=404, detail="This good doesn't exist")
    return crud.delete_good(db, db_good)

@app.patch("/goods/{good_id}", response_model=schemas.Good)  # Изменение
def update_good(good_id: int, good: schemas.GoodUpdate, db: Session = Depends(get_db)):
    db_good = crud.get_good(db, good_id)
    if not db_good:
        raise HTTPException(status_code=404, detail="This good doesn't exist")
    return crud.update_good(db, good, db_good)

@app.get("/categories/", response_model=List[schemas.Category])  # Просмотр списка категорий
def read_categories(db: Session = Depends(get_db)):
    categories = crud.get_categories(db, skip=0, limit=100)
    return categories

@app.get("/categories/{category_id}", response_model=schemas.Category)  # Поиск по id 
def read_category(category_id: int, db: Session = Depends(get_db)):
    category = crud.get_category(db, category_id)
    return category
 
@app.post("/categories/", response_model=schemas.Category)  # Создание 
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return crud.create_category(db, category)

@app.delete("/categories/{category_id}")  # Удаление 
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = crud.get_category(db, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="This category doesn't exist")
    return crud.delete_category(db, db_category)

@app.patch("/categories/{category_id}", response_model=schemas.Category)
def update_category(category_id: int, category: schemas.CategoryUpdate, db: Session = Depends(get_db)):
    db_category = crud.get_category(db, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="This category doesn't exist")
    return crud.update_category(db, category, db_category)

@app.get("/brands/", response_model=List[schemas.Brand])  # Просмотр списка брендов
def read_brands(db: Session = Depends(get_db)):
    brands = crud.get_brands(db, skip=0, limit=100)
    return brands

@app.get("/brands/{brand_id}", response_model=schemas.Brand)  # Поиск по id 
def read_brand(brand_id: int, db: Session = Depends(get_db)):
    brand = crud.get_brand(db, brand_id)
    return brand
 
@app.post("/brands/", response_model=schemas.Brand)  # Создание 
def create_brand(brand: schemas.BrandCreate, db: Session = Depends(get_db)):
    return crud.create_brand(db, brand)

@app.delete("/brands/{brand_id}")  # Удаление 
def delete_brand(brand_id: int, db: Session = Depends(get_db)):
    db_brand = crud.get_brand(db, brand_id)
    if not db_brand:
        raise HTTPException(status_code=404, detail="This brand doesn't exist")
    return crud.delete_brand(db, db_brand)

@app.patch("/brands/{brand_id}", response_model=schemas.Brand)
def update_brand(brand_id: int, brand: schemas.BrandUpdate, db: Session = Depends(get_db)):
    db_brand = crud.get_brand(db, brand_id)
    if not db_brand:
        raise HTTPException(status_code=404, detail="This brand doesn't exist")
    return crud.update_brand(db, brand, db_brand)


@app.post("/goods/{good_id}/images", response_model=schemas.Image)
def upload_image(good_id: int, file: UploadFile, db: Session = Depends(get_db)):
   file_location = crud.upload_image(file)
   return crud.create_upload_image(db, good_id, file_location)

@app.delete("/goods/{good_id}/images/{image_id}")
def delete_image(image_id: int, db: Session = Depends(get_db)):
    db_image = crud.get_image(db, image_id)
    if not db_image:
        raise HTTPException(status_code=404, detail="This image doesn't exist")
    return crud.delete_image(db, db_image)

@app.get("/goods/{good_id}/images", response_model=List[schemas.Image])  # Просмотр списка 
def read_images(good_id: int, db: Session = Depends(get_db)):
    good = crud.get_good(db, good_id)
    return good.images

