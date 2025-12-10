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


@app.post("/room-types", response_model=schemas.RoomType)
def create_room_type(
    room_type: schemas.RoomTypeCreate,
    db: Session = Depends(get_db),
):
    # Ensure hotel exists (basic check)
    hotel = db.query(models.Hotel).filter(models.Hotel.id == room_type.hotel_id).first()
    if hotel is None:
        raise ValueError("Hotel not found")  # we’ll improve error handling later

    db_room_type = models.RoomType(
        hotel_id=room_type.hotel_id,
        name=room_type.name,
        capacity=room_type.capacity,
        base_price=room_type.base_price,
    )
    db.add(db_room_type)
    db.commit()
    db.refresh(db_room_type)
    return db_room_type


@app.get("/room-types", response_model=list[schemas.RoomType])
def list_room_types(db: Session = Depends(get_db)):
    room_types = db.query(models.RoomType).all()
    return room_types


@app.get("/hotels/{hotel_id}/room-types", response_model=list[schemas.RoomType])
def list_room_types_for_hotel(hotel_id: int, db: Session = Depends(get_db)):
    room_types = (
        db.query(models.RoomType)
        .filter(models.RoomType.hotel_id == hotel_id)
        .all()
    )
    return room_types
