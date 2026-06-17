from sqlalchemy.orm import Session
from . import models

def get_datasets(db: Session):
    return db.query(models.Dataset).all()

def create_dataset(db: Session, filename: str, path: str):
    new_dataset = models.Dataset(filename=filename, filepath=path)
    db.add(new_dataset)
    db.commit()
    return new_dataset

def delete_dataset(db: Session, dataset_id: int):
    dataset = db.query(models.Dataset).filter(models.Dataset.id == dataset_id).first()
    if dataset:
        db.delete(dataset)
        db.commit()
    return True
