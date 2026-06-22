from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_admin_user
from app.models.category import Category
from app.models.user import User
from app.schemas.category_schema import CategoryCreate, CategoryOut

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=list[CategoryOut])
def get_all_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()


@router.get("/{id}", response_model=CategoryOut)
def get_category(id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.post("/", response_model=CategoryOut)
def create_category(
    request: CategoryCreate, admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    existing = db.query(Category).filter(Category.name == request.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")
    new_category = Category(name=request.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@router.put("/{id}", response_model=CategoryOut)
def update_category(
    id: int, request: CategoryCreate, admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    category = db.query(Category).filter(Category.id == id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    category.name = request.name
    db.commit()
    db.refresh(category)
    return category


@router.delete("/{id}")
def delete_category(
    id: int, admin: User = Depends(get_admin_user), db: Session = Depends(get_db),
):
    category = db.query(Category).filter(Category.id == id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return {"message": "Category deleted"}
