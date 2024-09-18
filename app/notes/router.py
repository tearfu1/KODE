from fastapi import APIRouter, Depends
from app.notes.dao import NoteDAO
from app.notes.rb import RBNote
from app.notes.schemas import SNote

router = APIRouter(prefix='/notes', tags=['Interaction with Notes'])


@router.get("/", summary="Get all notes")
async def get_all_notes(request_body: RBNote = Depends()) -> list[SNote]:
    return await NoteDAO().find_all(**request_body.to_dict())
