from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user, get_admin_user
from app.models.reaction import Reaction
from app.models.reaction_type import ReactionType
from app.models.post import Post
from app.models.user import User
from app.schemas.reaction_schema import ReactionTypeCreate, ReactionTypeOut, ReactionCreate, ReactionOut

router = APIRouter(tags=["Reactions"])


@router.get("/reaction-types", response_model=list[ReactionTypeOut])
def get_reaction_types(db: Session = Depends(get_db)):
    return db.query(ReactionType).all()


@router.post("/reaction-types", response_model=ReactionTypeOut)
def create_reaction_type(
    request: ReactionTypeCreate, admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    new_type = ReactionType(name=request.name)
    db.add(new_type)
    db.commit()
    db.refresh(new_type)
    return new_type


@router.get("/posts/{id}/reaction", response_model=list[ReactionOut])
def get_reactions(id: int, db: Session = Depends(get_db)):
    return db.query(Reaction).filter(Reaction.post_id == id).all()


@router.post("/posts/{id}/reaction", response_model=ReactionOut)
def add_reaction(
    id: int, request: ReactionCreate,
    user: User = Depends(get_current_user), db: Session = Depends(get_db),
):
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    existing = db.query(Reaction).filter(
        Reaction.post_id == id, Reaction.user_id == user.id
    ).first()
    if existing:
        existing.reaction_type_id = request.reaction_type_id
        db.commit()
        db.refresh(existing)
        return existing

    new_reaction = Reaction(
        post_id=id, user_id=user.id, reaction_type_id=request.reaction_type_id
    )
    db.add(new_reaction)
    db.commit()
    db.refresh(new_reaction)
    return new_reaction


@router.delete("/posts/{id}/reaction")
def remove_reaction(
    id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db),
):
    reaction = db.query(Reaction).filter(
        Reaction.post_id == id, Reaction.user_id == user.id
    ).first()
    if not reaction:
        raise HTTPException(status_code=404, detail="Reaction not found")
    db.delete(reaction)
    db.commit()
    return {"message": "Reaction removed"}
