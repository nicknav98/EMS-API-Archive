from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session):
    return db.query(models.User).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_hashed_password(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# ------------END OF User Functions----------------------------------------------------------------------------------------------------


def get_building(db: Session, building_id: int):
    return db.query(models.Building).filter(models.Building.id == building_id).first()


def get_building_by_name(db: Session, building_name: str):
    return db.query(models.Building).filter(models.Building.name == building_name).first()


def get_building_by_user(db: Session, user_id: int):
    return db.query(models.Building).filter(models.Building.user_id == user_id).first()


def get_buildings(db: Session):
    return db.query(models.Building).all()

# ------------END OF Building Functions----------------------------------------------------------------------------------------------------


def get_measurement_by_starttime(db: Session, starttime: str):
    return db.query(models.Measurement).filter(models.Measurement.starttime == starttime).first()

def get_measurement_by_building(db: Session, building_name: str):
    return db.query(models.Measurement).filter(models.Measurement.building_name == building_name).all()

def get_measurements(db: Session):
    return db.query(models.Measurement).all()

# ------------END OF Measurement Functions----------------------------------------------------------------------------------------------------


