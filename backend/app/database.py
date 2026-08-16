import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base


DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    db_user = os.getenv("DB_USER", "devops_user")
    db_password = os.getenv("DB_PASSWORD", "devops_password")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "devops_db")

    DATABASE_URL = (
        f"postgresql+psycopg://{db_user}:{db_password}"
        f"@{db_host}:{db_port}/{db_name}"
    )

engine = create_engine(DATABASE_URL)

Base = declarative_base()