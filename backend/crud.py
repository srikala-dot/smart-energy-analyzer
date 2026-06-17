from sqlalchemy.orm import Session
from . import models

def get_datasets(db: Session):
    return db.query(models.Dataset).all()

def create_dataset(db: Session, filename: str, path: str):
    new_entry = models.Dataset(filename=filename, filepath=path)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

# THIS IS THE FUNCTION YOUR APP IS CURRENTLY FAILING TO FIND
def delete_dataset(db: Session, dataset_id: int):
    entry = db.query(models.Dataset).filter(models.Dataset.id == dataset_id).first()
    if entry:
        db.delete(entry)
        db.commit()
        return True
    return False
