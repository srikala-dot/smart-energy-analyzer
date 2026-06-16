from pydantic import BaseModel
from datetime import datetime

class DatasetBase(BaseModel):
    filename: str
    filepath: str

class DatasetCreate(DatasetBase):
    pass

class Dataset(DatasetBase):
    id: int
    uploaded_at: datetime

    class Config:
        orm_mode = True
