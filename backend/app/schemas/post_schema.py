import re
from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional


class PostCreate(BaseModel):
    title: str
    content: str
    category_id: int
    summary: Optional[str] = None
    cover_image_url: Optional[str] = None

    @field_validator("title")
    def title_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()

    @field_validator("content")
    def content_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Content cannot be empty")
        return v.strip()


class PostOut(BaseModel):
    id: int
    title: str
    content: str
    summary: Optional[str] = None
    cover_image_url: Optional[str] = None
    views: Optional[int] = 0
    user_id: int
    category_id: int
    author_name: Optional[str] = None
    category_name: Optional[str] = None
    reading_time: Optional[int] = 1
    comment_count: Optional[int] = 0
    reaction_count: Optional[int] = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PostListResponse(BaseModel):
    posts: list[PostOut]
    total: int
    page: int
    pages: int


def calculate_reading_time(content: str) -> int:
    """Strip HTML tags and estimate reading time (200 words per minute)."""
    text = re.sub(r"<[^>]*>", "", content)
    words = len(text.split())
    return max(1, round(words / 200))
