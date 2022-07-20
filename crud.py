from sqlalchemy.orm import Session

import models
import schemas
import password


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate, password_hashed: schemas.UserDB):
    db_user = models.User(email=user.email, password=password_hashed)
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


def get_building_by_user(db: Session, user_id: int):
    return db.query(models.Building).filter(models.Building.user_id == user_id).first()


def get_buildings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Building).offset(skip).limit(limit).all()


def create_user_building(db: Session, user_id: int, building: schemas.BuildingCreate):
    db_building = models.Building(name=building.name, location=building.location,
                                  is_pv_installed=building.is_pv_installed, user_id=user_id)
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

def create_access_token(db: Session, user_id: int, expires: float = 3600):
    access_token = models.AccessToken(user_id=user_id)
    db.add(access_token)
    db.commit()
    db.refresh(access_token)
    return access_token
