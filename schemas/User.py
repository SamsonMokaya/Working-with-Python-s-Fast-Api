from typing import List
from pydantic import BaseModel


class UserInfoBase(BaseModel):
    username: str
    email: str


class UserCreate(UserInfoBase):
    password: str

class UserCheck(BaseModel):
    email: str
    password: str
class UserInfo(UserCreate):
    id: int

    class Config:
        orm_mode = True


