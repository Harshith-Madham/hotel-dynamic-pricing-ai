from fastapi import FastAPI

app = FastAPI(title="SmartRate AI - Hotel Pricing API")


@app.get("/")
def read_root():
    return {"message": "SmartRate AI backend is running 🚀"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
