from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TestCreate(BaseModel):
    name: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        orm_mode = True


class TestResponse(TestCreate):
    id: int
    created_at: datetime
    # created_by: int

    class Config:
        orm_mode = True
