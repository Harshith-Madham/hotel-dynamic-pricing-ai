import random
from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import models


def reset_database(db: Session) -> None:
    """Optional: clear existing data so seeding is repeatable."""
    db.query(models.Booking).delete()
    db.query(models.RoomType).delete()
    db.query(models.Hotel).delete()
    db.commit()


def seed_hotels(db: Session):
    hotels_data = [
        {"name": "SmartStay Downtown", "city": "Hyderabad", "country": "India"},
        {"name": "Skyline Suites", "city": "Kansas City", "country": "USA"},
        {"name": "Oceanview Resort", "city": "Miami", "country": "USA"},
    ]

    hotels = []
    for h in hotels_data:
        hotel = models.Hotel(**h)
        db.add(hotel)
        hotels.append(hotel)

    db.commit()
    for h in hotels:
        db.refresh(h)
    return hotels


def seed_room_types(db: Session, hotels):
    room_types = []

    for hotel in hotels:
        room_type_configs = [
            ("Standard", 2, 80.0),
            ("Deluxe", 2, 120.0),
            ("Suite", 4, 200.0),
        ]
        for name, capacity, base_price in room_type_configs:
            rt = models.RoomType(
                hotel_id=hotel.id,
                name=name,
                capacity=capacity,
                base_price=base_price,
            )
            db.add(rt)
            room_types.append(rt)

    db.commit()
    for rt in room_types:
        db.refresh(rt)
    return room_types


def seed_bookings(db: Session, hotels, room_types, days_back: int = 120, days_forward: int = 60):
    """
    Create synthetic bookings in a date range around today.
    """
    today = date.today()
    bookings = []

    # Index room types by hotel for convenience
    rts_by_hotel = {}
    for rt in room_types:
        rts_by_hotel.setdefault(rt.hotel_id, []).append(rt)

    for hotel in hotels:
        for day_offset in range(-days_back, days_forward):
            check_in = today + timedelta(days=day_offset)
            check_out = check_in + timedelta(days=random.choice([1, 2, 3]))
            booking_date = check_in - timedelta(days=random.randint(1, 30))

            # Probability of having bookings depends on weekday vs weekend
            weekday = check_in.weekday()  # 0=Mon, 6=Sun
            base_prob = 0.3
            if weekday in (4, 5):  # Friday, Saturday
                base_prob = 0.7

            # Random chance of 0–3 bookings for this date
            num_bookings = 0
            if random.random() < base_prob:
                num_bookings = random.randint(1, 3)

            for _ in range(num_bookings):
                room_type = random.choice(rts_by_hotel[hotel.id])

                # Price fluctuation around base_price
                # Weekends = more expensive, weekdays = slightly cheaper
                price_multiplier = 1.0
                if weekday in (4, 5):
                    price_multiplier += random.uniform(0.2, 0.5)
                else:
                    price_multiplier += random.uniform(-0.1, 0.2)

                price_sold = round(room_type.base_price * price_multiplier, 2)

                status = random.choices(
                    ["confirmed", "cancelled", "no-show"],
                    weights=[0.75, 0.2, 0.05],
                    k=1,
                )[0]

                booking = models.Booking(
                    hotel_id=hotel.id,
                    room_type_id=room_type.id,
                    booking_date=booking_date,
                    check_in_date=check_in,
                    check_out_date=check_out,
                    status=status,
                    price_sold=price_sold,
                )
                db.add(booking)
                bookings.append(booking)

    db.commit()
    return bookings


def main():
    db = SessionLocal()
    try:
        print("Resetting database...")
        reset_database(db)

        print("Seeding hotels...")
        hotels = seed_hotels(db)

        print("Seeding room types...")
        room_types = seed_room_types(db, hotels)

        print("Seeding bookings...")
        bookings = seed_bookings(db, hotels, room_types)

        print(f"Seed complete: {len(hotels)} hotels, {len(room_types)} room types, {len(bookings)} bookings.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
