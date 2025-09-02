from fastapi import FastAPI
from app.api.v1.endpoints import habits

app = FastAPI(
    title="Personal Wellness tracker API",
    description="A backend API for tracking personal wellness data.",
    version="1.0.0"
)

# Include the habits router. This makes all habit endpoints available.
app.include_router(habits.router, prefix ="/v1/habits", tags=["habits"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Personal Wellness Tracker API"}