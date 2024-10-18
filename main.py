from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated, Optional
from datetime import datetime, timezone
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

class NoteCreate(BaseModel):
    note_value: Optional[str] = None
    note_title: Optional[str] = None

class NoteResponse(BaseModel):
    id: int
    note_value: Optional[str] = None
    note_title: Optional[str] = None
    date_created: datetime

    class Config:
        orm_mode = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/")
async def root():
    return {"message": "Welcome to RetainSure!"}

@app.post("/notes/", response_model=NoteResponse)
async def create_note(note: NoteCreate, db: db_dependency):
    db_note = models.Note(note_value=note.note_value, note_title=note.note_title, date_created=datetime.now(timezone.utc))
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@app.get("/notes/", response_model=List[NoteResponse])
async def get_notes(db: db_dependency):
    notes = db.query(models.Note).all()
    return notes

@app.get("/notes/{note_id}", response_model=NoteResponse)
async def get_note_by_id(note_id: int, db: db_dependency):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@app.put("/notes/{note_id}", response_model=NoteResponse)
async def update_note_by_id(note_id: int, note: NoteCreate, db: db_dependency):
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    db_note.note_value = note.note_value
    db.commit()
    db.refresh(db_note)
    return db_note

@app.delete("/notes/{note_id}")
async def delete_note_by_id(note_id: int, db: db_dependency):
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(db_note)
    db.commit()
    return {"message": "Note deleted successfully"}