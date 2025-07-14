from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import database, models

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ml service ok"}

@app.get("/data")
def read_data(db: Session = Depends(database.SessionLocal)):
    return db.query(models.ExampleModel).all()
