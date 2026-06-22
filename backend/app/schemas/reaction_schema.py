from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ReactionTypeCreate(BaseModel):
    name: str


class ReactionTypeOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class ReactionCreate(BaseModel):
    reaction_type_id: int


class ReactionOut(BaseModel):
    id: int
    post_id: int
    user_id: int
    reaction_type_id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
