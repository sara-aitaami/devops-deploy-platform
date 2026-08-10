import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://devops_user:devops_password@localhost:5432/devops_db",
)

engine = create_engine(DATABASE_URL)

Base = declarative_base()