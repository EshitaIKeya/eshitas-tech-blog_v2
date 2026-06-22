from math import ceil
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_admin_user
from app.models.post import Post
from app.models.user import User
from app.models.category import Category
from app.models.comment import Comment
from app.models.reaction import Reaction
from app.schemas.post_schema import PostCreate, PostOut, PostListResponse, calculate_reading_time
from app.utils.ai_summary import generate_summary

router = APIRouter(prefix="/posts", tags=["Posts"])


def post_with_extras(post, db):
    """Add author name, category name, reading time, and counts to a post."""
    author = db.query(User).filter(User.id == post.user_id).first()
    category = db.query(Category).filter(Category.id == post.category_id).first()

    data = PostOut.model_validate(post)
    data.author_name = author.username if author else "Unknown"
    data.category_name = category.name if category else "Uncategorized"
    data.reading_time = calculate_reading_time(post.content)
    data.comment_count = db.query(Comment).filter(Comment.post_id == post.id).count()
    data.reaction_count = db.query(Reaction).filter(Reaction.post_id == post.id).count()
    return data


@router.get("/", response_model=PostListResponse)
def get_all_posts(
    page: int = 1, limit: int = 10, category_id: int = None,
    q: str = None, db: Session = Depends(get_db),
):
    """Get posts with pagination, optional category filter, and search."""
    query = db.query(Post)
    if category_id:
        query = query.filter(Post.category_id == category_id)
    if q:
        query = query.filter(Post.title.ilike(f"%{q}%"))

    total = query.count()
    pages = max(1, ceil(total / limit))
    posts = query.order_by(Post.created_at.desc()).offset((page - 1) * limit).limit(limit).all()

    return {
        "posts": [post_with_extras(p, db) for p in posts],
        "total": total, "page": page, "pages": pages,
    }


@router.get("/{id}", response_model=PostOut)
def get_post(id: int, db: Session = Depends(get_db)):
    """Get a single post and increment its view count."""
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Increment view count
    post.views = (post.views or 0) + 1
    db.commit()
    db.refresh(post)

    return post_with_extras(post, db)


@router.post("/", response_model=PostOut)
def create_post(
    request: PostCreate, admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    new_post = Post(
        title=request.title, content=request.content,
        summary=request.summary, cover_image_url=request.cover_image_url,
        user_id=admin.id, category_id=request.category_id,
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return post_with_extras(new_post, db)


@router.put("/{id}", response_model=PostOut)
def update_post(
    id: int, request: PostCreate, admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post.title = request.title
    post.content = request.content
    post.category_id = request.category_id
    if request.summary is not None:
        post.summary = request.summary
    if request.cover_image_url is not None:
        post.cover_image_url = request.cover_image_url
    db.commit()
    db.refresh(post)
    return post_with_extras(post, db)


@router.delete("/{id}")
def delete_post(
    id: int, admin: User = Depends(get_admin_user), db: Session = Depends(get_db),
):
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.query(Comment).filter(Comment.post_id == id).delete()
    db.query(Reaction).filter(Reaction.post_id == id).delete()
    db.delete(post)
    db.commit()
    return {"message": "Post deleted"}


@router.post("/{id}/generate-summary")
def generate_post_summary(
    id: int, admin: User = Depends(get_admin_user), db: Session = Depends(get_db),
):
    """Admin-only: call Groq's API to generate a 2-3 sentence summary."""
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    try:
        summary = generate_summary(post.content)
        post.summary = summary
        db.commit()
        return {"summary": summary}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI summary failed: {str(e)}")
