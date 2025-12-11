import os
from typing import List

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

from app.ml.data_prep import load_booking_data


def engineer_features(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series, List[str]]:
    """
    Take raw joined bookings DataFrame and return:
    X (features), y (target), feature_columns (list of feature names).
    """

    # Only use confirmed bookings for training (price actually realized)
    df = df[df["status"] == "confirmed"].copy()

    # Convert dates to datetime
    df["booking_date"] = pd.to_datetime(df["booking_date"])
    df["check_in_date"] = pd.to_datetime(df["check_in_date"])
    df["check_out_date"] = pd.to_datetime(df["check_out_date"])

    # --- Basic time-based features ---
    df["stay_length"] = (df["check_out_date"] - df["check_in_date"]).dt.days
    df["booking_window"] = (df["check_in_date"] - df["booking_date"]).dt.days
    df["check_in_weekday"] = df["check_in_date"].dt.weekday  # 0=Mon, 6=Sun
    df["is_weekend_checkin"] = df["check_in_weekday"].isin([4, 5]).astype(int)

    # Target
    y = df["price_sold"]

    # Start with numeric features
    feature_cols = [
        "base_price",
        "room_capacity",
        "stay_length",
        "booking_window",
        "check_in_weekday",
        "is_weekend_checkin",
    ]

    # Categorical features to one-hot encode
    cat_cols = ["city", "room_type_name"]

    df_cat = pd.get_dummies(df[cat_cols], prefix=cat_cols)
    X_num = df[feature_cols]

    X = pd.concat([X_num, df_cat], axis=1)
    all_feature_cols = list(X.columns)

    return X, y, all_feature_cols


def train_price_model():
    print("Loading data from database...")
    df = load_booking_data()
    print(f"Raw rows: {df.shape[0]}")

    X, y, feature_columns = engineer_features(df)
    print(f"Training rows after filtering: {X.shape[0]}")
    print(f"Number of features: {X.shape[1]}")

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Model
    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=None,
        random_state=42,
        n_jobs=-1,
    )

    print("Training model...")
    model.fit(X_train, y_train)

    # Evaluation
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print("\nModel evaluation:")
    print(f"  MAE: {mae:.2f}")
    print(f"  R^2: {r2:.3f}")

    # Save model and feature columns
    models_dir = os.path.join("app", "ml", "models")
    os.makedirs(models_dir, exist_ok=True)

    model_path = os.path.join(models_dir, "price_model.pkl")
    features_path = os.path.join(models_dir, "feature_columns.pkl")

    joblib.dump(model, model_path)
    joblib.dump(feature_columns, features_path)

    print(f"\nModel saved to: {model_path}")
    print(f"Feature columns saved to: {features_path}")


def main():
    train_price_model()


if __name__ == "__main__":
    main()
