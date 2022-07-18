from typing import List
from pydantic import BaseModel

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from jose import jwt, JWTError
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class BuildingBase(BaseModel):
    name: str
    location: str
    is_pv_installed: bool
    user_id: int

    class Config:
        orm_mode = True


class BuildingCreate(BuildingBase):
    pass


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    username: str
    password: str
    is_active: bool

    buildings: List[BuildingBase]

    class Config:
        orm_mode = True


class MeasurementBase(BaseModel):
    starttime: str
    endtime: str
    energy: int
    unit: str
    building_name: str

    class Config:
        orm_mode = True


class MeasurmementCreate(MeasurementBase):
    pass
