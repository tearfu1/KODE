from app.dao.base import BaseDAO
from app.notes.models import Note


class NoteDAO(BaseDAO):
    model = Note