from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app import models
from app.database import engine
from app import schemas
from app.dependencies import get_db


app = FastAPI(title="SmartRate AI - Hotel Pricing API")

# Create tables
models.Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message": "SmartRate AI backend is running 🚀"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/hotels", response_model=schemas.Hotel)
def create_hotel(hotel: schemas.HotelCreate, db: Session = Depends(get_db)):
    db_hotel = models.Hotel(
        name=hotel.name,
        city=hotel.city,
        country=hotel.country,
    )
    db.add(db_hotel)
    db.commit()
    db.refresh(db_hotel)
    return db_hotel


@app.get("/hotels", response_model=list[schemas.Hotel])
def list_hotels(db: Session = Depends(get_db)):
    hotels = db.query(models.Hotel).all()
    return hotels
