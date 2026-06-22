from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.role import Role
from app.schemas.auth_schema import RegisterSchema, LoginSchema, TokenSchema
from app.schemas.user_schema import ChangePasswordSchema
from app.utils.hashing import hash_password, verify_password
from app.utils.jwt_token import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register(request: RegisterSchema, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == request.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")
    if db.query(User).filter(User.email == request.email).first():
        raise HTTPException(status_code=400, detail="Email already taken")

    default_role = db.query(Role).filter(Role.role_name == "user").first()
    if not default_role:
        raise HTTPException(status_code=500, detail="Default role not found")

    new_user = User(
        username=request.username,
        email=request.email,
        hashed_password=hash_password(request.password),
        role_id=default_role.id,
    )
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}


@router.post("/login", response_model=TokenSchema)
def login(request: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
def get_me(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == user.role_id).first()
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role_id": user.role_id,
        "role_name": role.role_name if role else "unknown",
    }


@router.put("/change-password")
def change_password(
    request: ChangePasswordSchema,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not verify_password(request.old_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Current password is wrong")
    user.hashed_password = hash_password(request.new_password)
    db.commit()
    return {"message": "Password changed successfully"}
