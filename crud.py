from datetime import timedelta, datetime
from typing import Union

from jose import jwt
from sqlalchemy.orm import Session

import models
import schemas
import password


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate, password_hashed: schemas.UserDB):
    db_user = models.User(email=user.email, username=user.username, password=password_hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# ------------END OF User
# Functions----------------------------------------------------------------------------------------------------


def get_building(db: Session, building_id: int):
    return db.query(models.Building).filter(models.Building.id == building_id).first()


def get_building_by_name(db: Session, building_name: str):
    return db.query(models.Building).filter(models.Building.name == building_name).first()


def get_building_by_user(db: Session, username: str, skip: int = 0, limit: int = 100):
    return db.query(models.Building).filter(models.Building.username == username).offset(skip).limit(limit).all()


def get_buildings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Building).offset(skip).limit(limit).all()


def create_user_building(db: Session, username: str, building: schemas.BuildingCreate):
    db_building = models.Building(name=building.name, location=building.location,
                                  is_pv_installed=building.is_pv_installed, username=username)
    db.add(db_building)
    db.commit()
    db.refresh(db_building)
    return db_building


# ------------END OF Building
# Functions----------------------------------------------------------------------------------------------------


def get_measurement_by_starttime(db: Session, starttime: str):
    return db.query(models.Measurement).filter(models.Measurement.starttime == starttime).first()


def get_measurement_by_building(db: Session, building_name: str):
    return db.query(models.Measurement).filter(models.Measurement.building_name == building_name).all()


def get_measurements(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Measurement).offset(skip).limit(limit).all()


def create_measurement(db: Session, measurement: schemas.MeasurementCreate):
    db_measurement = models.Measurement(starttime=measurement.starttime, endtime=measurement.endtime,
                                        energy=measurement.energy, unit=measurement.unit,
                                        building_name=measurement.building_name)
    db.add(db_measurement)
    db.commit()
    db.refresh(db_measurement)
    return db_measurement


# ------------END OF Measurement
# Functions----------------------------------------------------------------------------------------------------

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, password.SECRET_KEY, algorithm=password.ALGORITHM)
    return encoded_jwt


def create_refresh_token(username: str):
    return create_access_token({'username': username}, expires_delta=timedelta(days=7))


def authenticate_user(db: Session, username: str, user_password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not password.verify_password(user_password, user.password):
        return False
    return user
