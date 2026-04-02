from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.user import User

router = APIRouter(prefix="/users", tags=["users"])


@router.post("")
def create_user(username: str, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    user = User(username=username)
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"id": user.id, "username": user.username}