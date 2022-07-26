from typing import Optional

from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import Session

import models
import crud
from password import verify_password


async def authenticate_user(db: Session, email: str, password: str):
    user = crud.get_user_by_email(db=db, email=email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


