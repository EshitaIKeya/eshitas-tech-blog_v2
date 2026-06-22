from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User
from app.models.role import Role
from app.utils.jwt_token import verify_token

security = HTTPBearer()


def get_db():
    """Give each request its own database session, then close it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    """Extract the Bearer token from the header and return the logged-in user."""
    token = credentials.credentials
    payload = verify_token(token)
    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_admin_user(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Check if the logged-in user has the admin role."""
    admin_role = db.query(Role).filter(Role.role_name == "admin").first()
    if not admin_role or user.role_id != admin_role.id:
        raise HTTPException(status_code=403, detail="Admin access only")
    return user
