from sqlalchemy.orm import Session
from . import models

# ... (keep your other existing functions like create_dataset and get_datasets here)

def delete_dataset(db: Session, dataset_id: int):
    """Removes a record from the database by its ID."""
    dataset = db.query(models.Dataset).filter(models.Dataset.id == dataset_id).first()
    if dataset:
        db.delete(dataset)
        db.commit()
    return dataset
