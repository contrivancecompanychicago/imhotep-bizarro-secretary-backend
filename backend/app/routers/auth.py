from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserLogin
from app.security import create_access_token, hash_password, verify_password
from app.models import User as UserModel

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(UserModel).filter(UserModel.email == user.email).first():
        raise HTTPException(status_code=409, detail="user already exists")

    new_user = UserModel(
        email=user.email,
        full_name=user.full_name,
        password_hash=hash_password(user.password),
        role=user.role,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "user created"}


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    user_record = db.query(UserModel).filter(UserModel.email == user.email).first()
    if not user_record or not verify_password(user.password, user_record.password_hash):
        raise HTTPException(status_code=401, detail="invalid credentials")

    token = create_access_token(user.email)
    return {"access_token": token, "token_type": "bearer"}
