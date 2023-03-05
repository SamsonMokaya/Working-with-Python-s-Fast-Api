from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, status
from models import models
from schemas import User


def get_user_by_username(db: Session, username: str):
    return db.query(models.UserInfo).filter(models.UserInfo.username == username).first()


def get_user_by_email(db: Session, email: str):
    user = db.query(models.UserInfo).filter(models.UserInfo.email == email).first()
    if user:
        return user
    return HTTPException(status_code=404, detail="User not found")

def get_user_by_email_and_password(db: Session, email: str, password: str):
    user = db.query(models.UserInfo).filter(models.UserInfo.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not password == user.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    return user

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.UserInfo).filter(models.UserInfo.id == user_id).first()


def get_all_users(db: Session):
    return db.query(models.UserInfo).all()


def create_user(db: Session, user: User.UserCreate):
    fake_hashed_password = user.password
    db_user = models.UserInfo(username=user.username, password=fake_hashed_password, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(user_id: int, db: Session, user: User.UserCreate):
    db_user = db.query(models.UserInfo).filter(models.UserInfo.id == user_id).first()
    if db_user:
        db_user.username = user.username
        db_user.password = user.password
        db_user.email = user.email
        db.commit()
        db.refresh(db_user)

        return db_user;
    return {"message": "User not found"}


def delete_user(db: Session, user_id: int):
    user = db.query(models.UserInfo).filter(models.UserInfo.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
