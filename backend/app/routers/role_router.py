from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_admin_user
from app.models.role import Role
from app.models.user import User
from app.schemas.role_schema import RoleCreate, RoleOut

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.get("/", response_model=list[RoleOut])
def get_all_roles(admin: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    return db.query(Role).all()


@router.post("/", response_model=RoleOut)
def create_role(
    request: RoleCreate, admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    existing = db.query(Role).filter(Role.role_name == request.role_name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Role already exists")
    new_role = Role(role_name=request.role_name)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role
