from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy_orm import relationship, Session

from database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(120), unique=True, index=True)
    hashed_password = Column(String(128))
    is_active = Column(Boolean, default=True)

    buildings = relationship("Building", backref="user")

    @classmethod
    def get_by_id(db: Session, user_id: int):
        return db.query.filter(User.id == user_id).first()

    @classmethod
    def get_by_email(db: Session, email: str):
        return db.query.filter(User.email == email).first()

    @classmethod
    def get_all_users(db: Session, skip: int = 0, limit: int = 100):
        return db.query(User).offset(skip).limit(limit).all()

