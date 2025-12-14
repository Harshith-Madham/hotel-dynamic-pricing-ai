from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models
from app.database import engine
from app import schemas
from app.dependencies import get_db
from app.ml.predict import predict_price_for_stay
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(title="SmartRate AI - Hotel Pricing API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
        raise HTTPException(status_code=404, detail="Hotel not found")


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


@app.post("/bookings", response_model=schemas.Booking)
def create_booking(
    booking: schemas.BookingCreate,
    db: Session = Depends(get_db),
):
    # Ensure hotel exists
    hotel = db.query(models.Hotel).filter(models.Hotel.id == booking.hotel_id).first()
    if hotel is None:
        raise HTTPException(status_code=404, detail="Hotel not found")

    # Ensure room type exists and belongs to the same hotel
    room_type = (
        db.query(models.RoomType)
        .filter(models.RoomType.id == booking.room_type_id)
        .first()
    )
    if room_type is None or room_type.hotel_id != booking.hotel_id:
        raise HTTPException(status_code=400, detail="Invalid room type for this hotel")

    db_booking = models.Booking(
        hotel_id=booking.hotel_id,
        room_type_id=booking.room_type_id,
        booking_date=booking.booking_date,
        check_in_date=booking.check_in_date,
        check_out_date=booking.check_out_date,
        status=booking.status,
        price_sold=booking.price_sold,
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


@app.get("/bookings", response_model=list[schemas.Booking])
def list_bookings(db: Session = Depends(get_db)):
    bookings = db.query(models.Booking).all()
    return bookings


@app.get("/hotels/{hotel_id}/bookings", response_model=list[schemas.Booking])
def list_bookings_for_hotel(hotel_id: int, db: Session = Depends(get_db)):
    bookings = (
        db.query(models.Booking)
        .filter(models.Booking.hotel_id == hotel_id)
        .all()
    )
    return bookings


@app.post("/price-recommendation", response_model=schemas.PriceRecommendationResponse)
def get_price_recommendation(
    payload: schemas.PriceRecommendationRequest,
    db: Session = Depends(get_db),
):
    # Fetch hotel
    hotel = db.query(models.Hotel).filter(models.Hotel.id == payload.hotel_id).first()
    if hotel is None:
        raise HTTPException(status_code=404, detail="Hotel not found")

    # Fetch room type
    room_type = (
        db.query(models.RoomType)
        .filter(models.RoomType.id == payload.room_type_id)
        .first()
    )
    if room_type is None or room_type.hotel_id != payload.hotel_id:
        raise HTTPException(status_code=400, detail="Invalid room type for this hotel")

    # Use ML model to predict a price
    model_price = predict_price_for_stay(
        city=hotel.city,
        room_type_name=room_type.name,
        base_price=room_type.base_price,
        room_capacity=room_type.capacity,
        check_in_date=payload.check_in_date,
        stay_length=payload.stay_length,
        booking_window=payload.booking_window,
    )

    # Simple business rule: clamp around base price
    lower_bound = room_type.base_price * 0.7
    upper_bound = room_type.base_price * 1.8
    recommended_price = max(lower_bound, min(model_price, upper_bound))

    return schemas.PriceRecommendationResponse(
        hotel_id=payload.hotel_id,
        room_type_id=payload.room_type_id,
        check_in_date=payload.check_in_date,
        recommended_price=round(recommended_price, 2),
        model_price=round(model_price, 2),
        base_price=room_type.base_price,
        currency="USD",  # or make this configurable later
    )
