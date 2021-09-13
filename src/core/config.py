import os
from logging import config as logging_config

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)

PROJECT_NAME = os.getenv("PROJECT_NAME", "movies")

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", 15436)
POSTGRES_DB_NAME = os.getenv("POSTGRES_DB_NAME", "postgres")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "94c3b047-d080-4b77-bd10-8cafea78e828")


SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@" \
                          f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB_NAME}"

JWT_SECRET = os.getenv("JWT_SECRET", "dev_secret")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
