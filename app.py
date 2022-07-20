from datetime import time, timedelta

from fastapi import FastAPI, Depends, HTTPException
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError

import crud
import models
import schemas
import password
import authentication
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from typing import List

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/register', response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: SessionLocal = Depends(get_db)):
    hashed_password = password.get_password_hash(user.password)
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    return crud.create_user(db=db, user=user, password_hashed=hashed_password)


@app.get('/users/', response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get('/users/{user_id}', response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post('/users/{user_id}/buildings/', response_model=schemas.Building)
def create_user_building(user_id: int, building: schemas.BuildingCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.create_user_building(db=db, user_id=user_id, building=building)


@app.get("/buildings/", response_model=List[schemas.Building])
def read_buildings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    buildings = crud.get_buildings(db, skip=skip, limit=limit)
    return buildings


@app.post("/measurements/", response_model=schemas.Measurement)
def create_measurement(measurement: schemas.MeasurementCreate, db: Session = Depends(get_db)):
    return crud.create_measurement(db=db, measurement=measurement)


@app.get("/measurements/", response_model=List[schemas.Measurement])
def read_measurements(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    measurements = crud.get_measurements(db, skip=skip, limit=limit)
    return measurements


@app.post("/token", response_model=schemas.Token)
async def create_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=form_data.username)
    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    hashed_password = user.hashed_password
    if not password.verify_password(plain_password=form_data.password, hashed_password=hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=30)
    access_token_expires_in_int = access_token_expires.total_seconds()
    access_token = crud.create_access_token(db, user_id=user.id, expires=access_token_expires_in_int)
    return {"access_token": access_token, "token_type": "bearer"}
