from fastapi import FastAPI, HTTPException, Depends
from typing import Annotated, List
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, engine
import models
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://crema-web.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

class CafeBase(BaseModel):
    cafe_name: str
    cafe_address: str
    cafe_city: str
    cafe_state: str
    cafe_zip: str
    cafe_phone: str
    cafe_website: str
    cafe_hours: str
    cafe_photo: str
    capp_photo: str
    cafe_long: float
    cafe_lat: float

class CafeModel(CafeBase):
    id: int

    class Config:
        orm_mode = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

models.Base.metadata.create_all(bind=engine)

@app.post("/cafes/", response_model=CafeModel)
async def create_cafe(cafe: CafeBase, db: db_dependency):
    db_cafe = models.Cafe(**cafe.dict())
    db.add(db_cafe)
    db.commit()
    db.refresh(db_cafe)
    return db_cafe

@app.get("/cafes/", response_model=List[CafeModel])
async def read_cafes(db: db_dependency, skip: int = 0, limit: int = 100):
    cafes = db.query(models.Cafe).offset(skip).limit(limit).all()
    return cafes 

@app.put("/cafes/{cafe_id}", response_model=CafeModel)
async def update_cafe(cafe_id: int, cafe: CafeBase, db: db_dependency):
    db_cafe = db.query(models.Cafe).filter(models.Cafe.id == cafe_id).first()
    
    if not db_cafe:
        raise HTTPException(status_code=404, detail="Cafe not found")
    
    # Update fields from the incoming model
    for key, value in cafe.dict().items():
        setattr(db_cafe, key, value)

    db.commit()
    db.refresh(db_cafe)
    return db_cafe

@app.delete("/cafes/{cafe_id}", response_model=CafeModel)
async def delete_cafe(cafe_id: int, db: db_dependency):
    # Fetch the transaction with the given id
    db_cafe = db.query(models.Cafe).filter(models.Cafe.id == cafe_id).first()
    
    if not db_cafe:
        raise HTTPException(status_code=404, detail="Cafe not found")
    
    db.delete(db_cafe)
    db.commit()
    return db_cafe