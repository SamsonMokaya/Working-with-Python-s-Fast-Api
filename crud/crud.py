
from sqlalchemy.orm import Session

from models import models
from schemas import schemas


def get_user_by_username(db: Session, username: str):
    return db.query(models.UserInfo).filter(models.UserInfo.username == username).first()

def get_all_users(db: Session):
    return db.query(models.UserInfo).all()

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.UserInfo(username=user.username, password=fake_hashed_password, fullname=user.fullname)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user