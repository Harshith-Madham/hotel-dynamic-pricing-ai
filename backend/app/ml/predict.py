import os
from datetime import date
from typing import List

import numpy as np
import pandas as pd
import joblib


# Lazy-loaded globals
_model = None
_feature_columns: List[str] | None = None


def _load_model_and_features():
    global _model, _feature_columns

    if _model is not None and _feature_columns is not None:
        return _model, _feature_columns

    models_dir = os.path.join("app", "ml", "models")
    model_path = os.path.join(models_dir, "price_model.pkl")
    features_path = os.path.join(models_dir, "feature_columns.pkl")

    _model = joblib.load(model_path)
    _feature_columns = joblib.load(features_path)

    return _model, _feature_columns


def _build_feature_row(
    city: str,
    room_type_name: str,
    base_price: float,
    room_capacity: int,
    check_in_date: date,
    stay_length: int,
    booking_window: int,
) -> pd.DataFrame:
    model, feature_columns = _load_model_and_features()

    # Start with all zeros
    data = {col: 0.0 for col in feature_columns}

    # Time features
    check_in_weekday = check_in_date.weekday()  # 0=Mon, 6=Sun
    is_weekend_checkin = 1 if check_in_weekday in (4, 5) else 0

    # Fill numeric features if present
    numeric_values = {
        "base_price": base_price,
        "room_capacity": room_capacity,
        "stay_length": stay_length,
        "booking_window": booking_window,
        "check_in_weekday": check_in_weekday,
        "is_weekend_checkin": is_weekend_checkin,
    }

    for col, val in numeric_values.items():
        if col in data:
            data[col] = float(val)

    # One-hot for city
    city_col = f"city_{city}"
    if city_col in data:
        data[city_col] = 1.0

    # One-hot for room type name
    rt_col = f"room_type_name_{room_type_name}"
    if rt_col in data:
        data[rt_col] = 1.0

    df = pd.DataFrame([data])
    return df


def predict_price_for_stay(
    city: str,
    room_type_name: str,
    base_price: float,
    room_capacity: int,
    check_in_date: date,
    stay_length: int,
    booking_window: int,
) -> float:
    model, _ = _load_model_and_features()
    X = _build_feature_row(
        city=city,
        room_type_name=room_type_name,
        base_price=base_price,
        room_capacity=room_capacity,
        check_in_date=check_in_date,
        stay_length=stay_length,
        booking_window=booking_window,
    )
    y_pred = model.predict(X)[0]
    return float(y_pred)
