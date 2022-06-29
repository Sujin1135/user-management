from sqlalchemy import Column, Integer, String
from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, max_length=320)
    password = Column(String, nullable=False, max_length=60)
    nickname = Column(String, nullable=True, max_length=20)
    name = Column(String, nullable=False, max_length=50)
    phone_number = Column(String, nullable=False, max_length=15)
