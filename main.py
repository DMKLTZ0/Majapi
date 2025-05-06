from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import datetime
import models
from database import SessionLocal, engine, Base

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class PostSchema(BaseModel):
    title: str
    content: str

class PostResponse(PostSchema):
    id: int
    class Config:
        orm_mode = True

class EntrySchema(BaseModel):
    type: str
    module: str
    content: str
    tags: str
    metadata: dict = {}

class EntryResponse(EntrySchema):
    id: int
    timestamp: datetime
    class Config:
        orm_mode = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "API z bazą danych działa!"}

@app.get("/posts", response_model=List[PostResponse])
def read_posts(db: Session = Depends(get_db)):
    return db.query(models.Post).all()

@app.get("/posts/{post_id}", response_model=PostResponse)
def read_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post nie istnieje")
    return post

@app.post("/posts", response_model=PostResponse)
def create_post(post: PostSchema, db: Session = Depends(get_db)):
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@app.put("/posts/{post_id}", response_model=PostResponse)
def update_post(post_id: int, post: PostSchema, db: Session = Depends(get_db)):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post nie istnieje")
    db_post.title = post.title
    db_post.content = post.content
    db.commit()
    db.refresh(db_post)
    return db_post

@app.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post nie istnieje")
    db.delete(db_post)
    db.commit()
    return {"message": "Post usunięty"}

@app.post("/entries", response_model=EntryResponse)
def create_entry(entry: EntrySchema, db: Session = Depends(get_db)):
    db_entry = models.Entry(**entry.dict())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

@app.get("/entries", response_model=List[EntryResponse])
def read_entries(db: Session = Depends(get_db)):
    return db.query(models.Entry).all()

@app.get("/entries/{entry_id}", response_model=EntryResponse)
def read_entry(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.Entry).filter(models.Entry.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry nie istnieje")
    return entry

@app.delete("/entries/{entry_id}")
def delete_entry(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.Entry).filter(models.Entry.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry nie istnieje")
    db.delete(entry)
    db.commit()
    return {"message": "Entry usunięty"}
