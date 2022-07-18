from fastapi import FastAPI
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


o2auth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

app = FastAPI()


@app.get("/")
async def hello_world():
    return {"hello": "world"}
