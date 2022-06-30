import logging

import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from app.configs.config import config

db_info = config.databases["inner"]
dns = "postgresql://{}:{}@{}:{}/{}".format(
    db_info["username"],
    db_info["password"],
    db_info["host"],
    db_info["port"],
    db_info["database"],
)
engine = create_engine(dns, echo=True)
DBSession = sessionmaker(bind=engine)


def get_db_session() -> Session:
    try:
        return DBSession()
    except Exception as e:
        logging.error("failed to connect db", e)


redis_info = config.databases["redis"]
