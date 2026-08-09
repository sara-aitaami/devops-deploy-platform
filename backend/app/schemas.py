from datetime import date

from pydantic import BaseModel


class ApplicationResponse(BaseModel):
    id: int
    name: str
    version: str
    status: str
    deployment_date: date

class ApplicationCreate(BaseModel):
    name: str
    version: str
    status: str
    deployment_date: date

class ApplicationUpdate(BaseModel):
    name: str
    version: str
    status: str
    deployment_date: date