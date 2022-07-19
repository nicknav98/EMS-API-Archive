from typing import List
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
    user_id = int

    measurements: List[MeasurementBase]

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    hashed_password: str


class User(UserBase):
    id: int
    is_active: bool

    buildings: List[BuildingBase]

    class Config:
        orm_mode = True
