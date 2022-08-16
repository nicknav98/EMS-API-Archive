from datetime import time, timedelta
from typing import Union
from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from fastapi_mqtt import FastMQTT, MQTTConfig

import crud
import models
import schemas
import password
import fileHandling
import authentication


from database import SessionLocal, engine
from sqlalchemy.orm import Session
from typing import List

models.Base.metadata.create_all(bind=engine)
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/token",
    scheme_name="JWT"
)


app = FastAPI()

mqtt_config = MQTTConfig(host="172.24.59.99",
                         port=1883,
                         keepalive=60,
                         username="",
                         password="",)

mqtt = FastMQTT(

    config=mqtt_config
)





mqtt.init_app(app)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, password.SECRET_KEY, algorithms=[password.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


@app.post('/register', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: SessionLocal = Depends(get_db)):
    hashed_password = password.get_password_hash(user.password)
    db_user = crud.get_user_by_email(db, email=user.email)
    db_username = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    if db_username:
        raise HTTPException(status_code=400, detail="User with this username already exists")
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


@app.post('/users/{username}/buildings/', response_model=schemas.Building)
def create_user_building(username: str, building: schemas.BuildingCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.create_user_building(db=db, username=username, building=building)


@app.get("/buildings/", response_model=List[schemas.Building])
def read_buildings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    buildings = crud.get_buildings(db, skip=skip, limit=limit)
    return buildings


@app.get("/users/me/buildings", response_model=List[schemas.Building])
def read_user_buildings(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_building = crud.get_building_by_user(db, username=current_user.username)
    return user_building


@app.post("/measurements/", response_model=schemas.Measurement)
def create_measurement(measurement: schemas.MeasurementCreate, db: Session = Depends(get_db)):
    return crud.create_measurement(db=db, measurement=measurement)


@app.get("/measurements/", response_model=List[schemas.Measurement])
def read_measurements(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    measurements = crud.get_measurements(db, skip=skip, limit=limit)
    return measurements


async def get_current_active_user(current_user: models.User = Depends(get_current_user)):
    if current_user.is_active is False:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, username=form_data.username, user_password=form_data.password)
    if not user:
        raise HTTPException(status_code=400,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})

    access_token_expires = timedelta(minutes=password.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crud.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=schemas.User)
async def get_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, password.SECRET_KEY, algorithms=[password.ALGORITHM])
        token_data = schemas.TokenData(username=payload.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Token is invalid", headers={"WWW-Authenticate": "Bearer"})
    user = crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found", headers={"WWW-Authenticate": "Bearer"})
    return user


@app.post("/users/files/measurements/")
async def file_to_database(building: str, file: UploadFile = File(...),
                           current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if file.content_type != "text/csv":
        raise HTTPException(status_code=400, detail="File is not csv")
    fileHandling.file_to_database(file, building)

    return {"message": "File uploaded"}


@app.get("/building-measurements/")
async def get_building_measurements(building_name: str, db: Session = Depends(get_db)):
    measurements = crud.get_measurement_by_building(db, building_name=building_name)
    return measurements


@mqtt.on_connect()
def connect_handler(client, userdata, flags, rc):
    client.subscribe("extapi/data/ehub")
    print("Connected to MQTT with result code ", client, userdata, flags, rc)


@mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    print("Message received: ", topic, payload, qos, properties)


@mqtt.on_disconnect()
def disconnect_handler(client, packet, exc=None):
    print("Disconnected from MQTT with reason code ", client, packet, exc)


@mqtt.on_subscribe()
def subscribed_handler(client, userdata, mid, granted_qos):
    print("Subscribed with result code ", client, userdata, mid, granted_qos)
