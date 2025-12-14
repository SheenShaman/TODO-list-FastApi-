from fastapi import FastAPI

from app.db.postgres.session import Base, engine
from app.routers import tasks, users, notes

app = FastAPI(title="FastAPI Project")


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(notes.router)


@app.get("/")
def health_check() -> dict[str, str]:
    return {"message": "Welcome!"}
