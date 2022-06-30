from sqlalchemy import Column, Integer, String
from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(320), nullable=False)
    password = Column(String(60), nullable=False)
    nickname = Column(String(20), nullable=True)
    name = Column(String(50), nullable=False)
    phone_number = Column(String(15), nullable=False)
