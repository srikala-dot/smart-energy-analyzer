from sqlalchemy.orm import Session
from . import models, schemas


def create_dataset(db: Session, filename: str, path: str):
    db_dataset = models.Dataset(filename=filename, filepath=path)
    db.add(db_dataset)
    db.commit()
    db.refresh(db_dataset)
    return db_dataset


def get_dataset(db: Session, dataset_id: int):
    return db.query(models.Dataset).filter(models.Dataset.id == dataset_id).first()


def get_datasets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Dataset).offset(skip).limit(limit).all()
