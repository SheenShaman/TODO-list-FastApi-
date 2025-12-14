from fastapi import APIRouter, Depends

from app import schemas
from app.utils import dependencies, exceptions
from app.db.postgres import models
from app.db.mongo.client import mongo_db

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("/create", response_model=schemas.Note)
async def create_note(
    note: schemas.NoteCreate,
    user: models.Users = Depends(dependencies.get_current_user),
):

    document = {
        "title": note.title,
        "content": note.content,
        "user_id": user.id,
        "task_id": note.task_id,
    }

    result = await mongo_db.note.insert_one(document)
    return {"id": str(result.inserted_id)}
