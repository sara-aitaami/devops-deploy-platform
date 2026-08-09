from sqlalchemy import Column, Integer, String, Date
from backend.app.database import Base


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    version = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False)
    deployment_date = Column(Date, nullable=False)