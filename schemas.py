from typing import List, Union
from pydantic import BaseModel


class MeasurementBase(BaseModel):
    starttime: str
    endtime: str
    energy: int
    unit: str
    building_name: str

    class Config:
        orm_mode = True


class MeasurementCreate(MeasurementBase):
    pass


class Measurement(MeasurementBase):
    class Config:
        orm_mode = True


class BuildingBase(BaseModel):
    name: str
    location: str
    is_pv_installed: bool

    class Config:
        orm_mode = True


class BuildingCreate(BuildingBase):
    pass


class Building(BuildingBase):
    id: int
    username = str

    measurements: List[MeasurementBase]

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    username: str
    password: str


class User(UserBase):
    id: int
    is_active: bool

    buildings: List[BuildingBase]

    class Config:
        orm_mode = True


class UserDB(User):
    hashed_password: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    token: str
    token_type: str

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    username: Union[str, None]

    class Config:
        orm_mode = True
