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
