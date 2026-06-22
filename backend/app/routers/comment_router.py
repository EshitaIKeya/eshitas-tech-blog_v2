from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.models.comment import Comment
from app.models.post import Post
from app.models.user import User
from app.models.role import Role
from app.schemas.comment_schema import CommentCreate, CommentOut

router = APIRouter(tags=["Comments"])


def comment_with_user(comment, db):
    user = db.query(User).filter(User.id == comment.created_by).first()
    data = CommentOut.model_validate(comment)
    data.commenter_name = user.username if user else "Unknown"
    return data


@router.get("/posts/{id}/comments", response_model=list[CommentOut])
def get_comments(id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    comments = db.query(Comment).filter(Comment.post_id == id).order_by(Comment.created_at.desc()).all()
    return [comment_with_user(c, db) for c in comments]


@router.post("/posts/{id}/comments", response_model=CommentOut)
def create_comment(
    id: int, request: CommentCreate,
    user: User = Depends(get_current_user), db: Session = Depends(get_db),
):
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    new_comment = Comment(content=request.content, post_id=id, created_by=user.id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return comment_with_user(new_comment, db)


@router.put("/comments/{id}", response_model=CommentOut)
def update_comment(
    id: int, request: CommentCreate,
    user: User = Depends(get_current_user), db: Session = Depends(get_db),
):
    comment = db.query(Comment).filter(Comment.id == id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.created_by != user.id:
        raise HTTPException(status_code=403, detail="Not your comment")
    comment.content = request.content
    db.commit()
    db.refresh(comment)
    return comment_with_user(comment, db)


@router.delete("/comments/{id}")
def delete_comment(
    id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db),
):
    comment = db.query(Comment).filter(Comment.id == id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    admin_role = db.query(Role).filter(Role.role_name == "admin").first()
    is_admin = admin_role and user.role_id == admin_role.id
    if comment.created_by != user.id and not is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    db.delete(comment)
    db.commit()
    return {"message": "Comment deleted"}
