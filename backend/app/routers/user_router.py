from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_admin_user
from app.models.user import User
from app.models.comment import Comment
from app.models.reaction import Reaction
from app.schemas.user_schema import UserOut

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserOut])
def get_all_users(admin: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    return db.query(User).all()


@router.get("/{id}", response_model=UserOut)
def get_user(id: int, admin: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{id}")
def delete_user(id: int, admin: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.query(Comment).filter(Comment.created_by == id).delete()
    db.query(Reaction).filter(Reaction.user_id == id).delete()
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}
