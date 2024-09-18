from fastapi import APIRouter, Depends
from app.notes.dao import NoteDAO
from app.notes.rb import RBNote
from app.notes.schemas import SNote, SNoteAdd, SNoteUpdate

router = APIRouter(prefix='/notes', tags=['Interaction with Notes'])


@router.get("/", summary="Get all notes")
async def get_all_notes(request_body: RBNote = Depends()) -> list[SNote]:
    return await NoteDAO().find_all(**request_body.to_dict())


@router.get("/{id}", summary="Get note by id")
async def get_note_by_id(id: int) -> SNote | dict:
    res = await NoteDAO().find_one_or_none_by_id(id)
    if res is None:
        return {'message': f"note not found. id: {id}"}
    return res


@router.post("/add")
async def add_note(note: SNoteAdd) -> dict:
    check = await NoteDAO.add(**note.dict())
    if check:
        return {"message": "success"}
    else:
        return {"message": "Error"}


@router.put("/edit/{id}")
async def edit_note(id: int, note: SNoteUpdate) -> dict:
    check = await NoteDAO.update(filter_by={"id": id},
                                 **note.dict(),
                                 )
    if check:
        return {"message": "success"}
    else:
        return {"message": "Error"}


@router.delete("/delete/{id}")
async def delete_major(id: int) -> dict:
    check = await NoteDAO.delete(id=id)
    if check:
        return {"message": f"success"}
    else:
        return {"message": "Error"}
