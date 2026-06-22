from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional


class CommentCreate(BaseModel):
    content: str

    @field_validator("content")
    def content_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Comment cannot be empty")
        return v.strip()


class CommentOut(BaseModel):
    id: int
    content: str
    post_id: int
    created_by: int
    commenter_name: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
