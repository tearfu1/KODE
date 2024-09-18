from fastapi import FastAPI
from utils import json_to_dict_list
from pathlib import Path, PurePosixPath
from typing import Optional

# Получаем путь к JSON
path_to_json = PurePosixPath(Path(__file__).resolve().parents[1]).joinpath('students.json')
print(path_to_json)
app = FastAPI()

@app.get("/notes")
def get_all_notes():
    return json_to_dict_list(path_to_json)

@app.get("/notes/{id}")
def get_all_students_course(id: int):
    notes = json_to_dict_list(path_to_json)
    return_list = []
    for note in notes:
        if note["note_id"] == id:
            return_list.append(note)
    return return_list