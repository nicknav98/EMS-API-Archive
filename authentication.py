from typing import Optional

from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import Session

import models
import crud
from password import verify_password


async def authenticate(db: Session, email: str, password: str):
    user = await crud.get_user_by_email(db=db, email=email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


async def create_access_token(db: Session, user_id: int, expires_delta: Optional[int] = None):
    token = crud.create_access_token(db=db, user_id=user_id, expires=expires_delta)
    return token
