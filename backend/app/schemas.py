from datetime import date
from pydantic import BaseModel


# ---------- HOTEL SCHEMAS ----------

class HotelBase(BaseModel):
    name: str
    city: str
    country: str


class HotelCreate(HotelBase):
    """Schema used when creating a new hotel."""
    pass


class Hotel(HotelBase):
    id: int

    class Config:
        from_attributes = True  # allows reading from ORM objects (SQLAlchemy)


# ---------- ROOM TYPE SCHEMAS ----------

class RoomTypeBase(BaseModel):
    hotel_id: int
    name: str
    capacity: int
    base_price: float


class RoomTypeCreate(RoomTypeBase):
    """Schema used when creating a new room type."""
    pass


class RoomType(RoomTypeBase):
    id: int

    class Config:
        from_attributes = True


# ---------- BOOKING SCHEMAS ----------

class BookingBase(BaseModel):
    hotel_id: int
    room_type_id: int
    booking_date: date
    check_in_date: date
    check_out_date: date
    status: str
    price_sold: float


class BookingCreate(BookingBase):
    """Schema used when creating a new booking."""
    pass


class Booking(BookingBase):
    id: int

    class Config:
        from_attributes = True

# ---------- PRICE RECOMMENDATION SCHEMAS ----------

class PriceRecommendationRequest(BaseModel):
    hotel_id: int
    room_type_id: int
    check_in_date: date
    stay_length: int = 1
    booking_window: int = 7  # days between booking creation and check-in


class PriceRecommendationResponse(BaseModel):
    hotel_id: int
    room_type_id: int
    check_in_date: date
    recommended_price: float
    model_price: float
    base_price: float
    currency: str = "USD"
