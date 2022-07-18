from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Session

from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String(120), unique=True, index=True)
    password = Column(String(128))
    is_active = Column(Boolean, default=True)

    buildings = relationship("Building", backref="user")




class Building(Base):
    __tablename__ = 'buildings'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), unique=True, index=True)
    location = Column(String(120))
    is_pv_installed = Column(Boolean, default=False)

    user = relationship("User", backref="buildings")


class Measurement(Base):
    __tablename__ = 'measurements'

    starttime = Column(String(120), primary_key=True, index=True)
    endtime = Column(String(120), primary_key=True, index=True)
    energy = Column(Integer)
    unit = Column(String(2))
    building_name = Column(String, ForeignKey('buildings.name'))


