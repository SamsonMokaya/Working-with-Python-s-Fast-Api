import uvicorn
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from models import models
from schemas import User
from crud import crud
from database import engine, SessionLocal
import secrets

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return crud.get_all_users(db)

@app.get("/user/{email}")
def get_user_by_email_password(email:str, password:str, db: Session = Depends(get_db)):
    return crud.get_user_by_email(db=db, email=email, password=password)


@app.post("/user", response_model=User.UserInfo)
def create_user(user: User.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@app.post("/login", response_model=User.UserInfo)
def login_user(user: User.UserCheck, db: Session = Depends(get_db)):
    return crud.get_user_by_email_and_password(db, email=user.email, password=user.password)


@app.put("/user/{user_id}", response_model=User.UserInfo)
def update_user(user_id: int, user: User.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail="Username not found")

    db_user = crud.update_user(db=db, user=user, user_id=user_id)
    return db_user



# @app.post("/user/{user_id}", response_model=User.UserInfo)
# def updhate_user(user_id: int, user: User.UserInfo, db: Session = Depends(get_db)):
#     # db_user = crud.get_user_by_id(db, user_id=user_id)
#     # if not db_user:
#     #     raise HTTPException(status_code=404, detail="User not found")
#     # db_user = crud.update_user(db=db, user=user, user_id=user_id)
#     return {"message": "User updated successfully"}


@app.delete("/user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return crud.delete_user(db=db, user_id=user_id)



# @app.post("/reset_password/")
# def forgot_password(email: email)


