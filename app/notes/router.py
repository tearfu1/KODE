from fastapi import APIRouter, Depends, HTTPException, status
from app.notes.dao import NoteDAO
from app.notes.rb import RBNote
from app.notes.schemas import SNote, SNoteAdd, SNoteUpdate
from fastapi.security import APIKeyHeader

API_KEYS = {
    "user1_api_key": "user1",
    "user2_api_key": "user2",
}

api_key_header = APIKeyHeader(name="X-API-Key")


def get_current_user(api_key: str = Depends(api_key_header)) -> str:
    user = API_KEYS.get(api_key)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )
    return user


router = APIRouter(prefix='/notes', tags=['Interaction with Notes'])


@router.get("/", summary="Get all notes")
async def get_all_notes(user: str = Depends(get_current_user), request_body: RBNote = Depends()) -> list[SNote]:
    return await NoteDAO().find_all(user, **request_body.to_dict())


@router.get("/{id}", summary="Get note by id")
async def get_note_by_id(id: int, user: str = Depends(get_current_user)) -> SNote | dict:
    res = await NoteDAO().find_one_or_none_by_id(user, id)
    if res is None:
        return {'message': f"note not found. id: {id}"}
    return res


@router.post("/add")
async def add_note(note: SNoteAdd, user: str = Depends(get_current_user)) -> dict:
    check = await NoteDAO.add(user, **note.dict())
    if check:
        return {"message": "success"}
    else:
        return {"message": "Error"}


@router.put("/edit/{id}")
async def edit_note(id: int, note: SNoteUpdate, user: str = Depends(get_current_user)) -> dict:
    check = await NoteDAO.update(user,
                                 filter_by={"id": id},
                                 **note.dict(),
                                 )
    if check:
        return {"message": "success"}
    else:
        return {"message": "Error"}


@router.delete("/delete/{id}")
async def delete_major(id: int, user: str = Depends(get_current_user)) -> dict:
    check = await NoteDAO.delete(user,id=id)
    if check:
        return {"message": f"success"}
    else:
        return {"message": "Error"}
