import pandas as pd

from app.database import engine


def load_booking_data() -> pd.DataFrame:
    """
    Load bookings joined with hotels and room_types into a single DataFrame.
    This will be the base dataset for our ML model.
    """
    query = """
    SELECT
        b.id AS booking_id,
        b.hotel_id,
        b.room_type_id,
        b.booking_date,
        b.check_in_date,
        b.check_out_date,
        b.status,
        b.price_sold,
        rt.name AS room_type_name,
        rt.capacity AS room_capacity,
        rt.base_price,
        h.name AS hotel_name,
        h.city,
        h.country
    FROM bookings b
    JOIN room_types rt ON b.room_type_id = rt.id
    JOIN hotels h ON b.hotel_id = h.id
    """
    df = pd.read_sql(query, con=engine)
    return df


def main():
    df = load_booking_data()
    print("Loaded booking dataset:")
    print(df.head())
    print()
    print(f"Shape: {df.shape}")
    print("Columns:", list(df.columns))


if __name__ == "__main__":
    main()
