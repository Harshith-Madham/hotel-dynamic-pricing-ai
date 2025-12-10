from fastapi import FastAPI

from app import models
from app.database import engine

app = FastAPI(title="SmartRate AI - Hotel Pricing API")

# Create tables
models.Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message": "SmartRate AI backend is running 🚀"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
