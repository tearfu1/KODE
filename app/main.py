from fastapi import FastAPI
from app.notes.router import router as notes_router

app = FastAPI()

@app.get("/")
def home_page():
    return {"message": "Maxim Vayda app"}

app.include_router(notes_router)
