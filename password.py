from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


SECRET_KEY = "92aec72c8a00d05a8638068394ba642523ff97c83cee9b2ddb5dd5fb2aea86d4"
ALGORITHM = "HS256"
