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
