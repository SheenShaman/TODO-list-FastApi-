from fastapi import FastAPI
from app.database import Base, engine
from app.routers import tasks, users

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Project")

# Include routes
app.include_router(tasks.router)
app.include_router(users.router)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Welcome!"}
