from fastapi import FastAPI

from app.database import engine, Base
from app.routers import tasks, users

app = FastAPI(title="FastAPI Project")


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Include routes
app.include_router(tasks.router)
app.include_router(users.router)


@app.get("/health_check")
def health_check() -> dict[str, str]:
    return {"message": "Welcome!"}
