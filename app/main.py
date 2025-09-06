from fastapi import FastAPI
from app.api.v1.endpoints import habits, users

app = FastAPI(
    title="Personal Wellness tracker API",
    description="A backend API for tracking personal wellness data.",
    version="1.0.0"
)


app.include_router(habits.router, prefix ="/v1/habits", tags=["habits"])
app.include_router(users.router, prefix="/v1/users", tags=["users"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Personal Wellness Tracker API"}