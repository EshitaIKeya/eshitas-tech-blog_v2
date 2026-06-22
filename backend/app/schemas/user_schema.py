from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    role_id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ChangePasswordSchema(BaseModel):
    old_password: str
    new_password: str
