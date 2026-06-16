import uvicorn
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
import os
from sqlalchemy.orm import Session
from . import models, schemas, crud, database
app = FastAPI(title="Smart Energy Backend", version="0.1.0")
# Create tables on startup
from . import models
models.Base.metadata.create_all(bind=database.engine)


# Dependency
# Ensure data directory exists
os.makedirs("./data", exist_ok=True)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

from fastapi.responses import FileResponse

@app.post("/upload-dataset/", response_model=schemas.Dataset)
async def upload_dataset(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Validate file type
    if not (file.filename.endswith('.csv') or file.filename.endswith('.md') or file.filename.endswith('.txt')):
        raise HTTPException(status_code=400, detail="File type not supported")
    # Save uploaded file to the data folder
    file_location = f"./data/{file.filename}"
    with open(file_location, "wb") as f:
        content = await file.read()
        f.write(content)
    db_dataset = crud.create_dataset(db=db, filename=file.filename, path=file_location)
    return db_dataset

@app.get("/datasets/", response_model=list[schemas.Dataset])
def list_datasets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    datasets = crud.get_datasets(db, skip=skip, limit=limit)
    return datasets

@app.get("/datasets/{dataset_id}", response_model=schemas.Dataset)
def get_dataset(dataset_id: int, db: Session = Depends(get_db)):
    db_dataset = crud.get_dataset(db, dataset_id=dataset_id)
    if db_dataset is None:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return db_dataset

@app.get("/datasets/{dataset_id}/download")
def download_dataset(dataset_id: int, db: Session = Depends(get_db)):
    db_dataset = crud.get_dataset(db, dataset_id=dataset_id)
    if db_dataset is None:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return FileResponse(db_dataset.path, media_type='text/csv', filename=db_dataset.filename)

# Simple health check
@app.get("/health")
def health_check():
    return {"status": "ok"}

