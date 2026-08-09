from typing import List

from fastapi import FastAPI
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.database import engine
from backend.app.models import Application
from backend.app.schemas import (
    ApplicationCreate,
    ApplicationResponse,
    ApplicationUpdate,
)

from fastapi import FastAPI, HTTPException

app = FastAPI(title="DevOps Deploy Platform API")


@app.get("/")
def root():
    return {"message": "DevOps Deploy Platform API is running"}


@app.get("/applications", response_model=List[ApplicationResponse])
def get_applications():
    with Session(engine) as session:
        result = session.execute(
            select(Application).order_by(Application.id)
        )

        applications = []

        for application in result.scalars():
            applications.append({
                "id": application.id,
                "name": application.name,
                "version": application.version,
                "status": application.status,
                "deployment_date": application.deployment_date
            })

        return applications

@app.get("/applications/{application_id}", response_model=ApplicationResponse)
def get_application(application_id: int):
    with Session(engine) as session:
        application = session.get(Application, application_id)

        if application is None:
            raise HTTPException(
                status_code=404,
                detail="Application not found"
            )

        return {
            "id": application.id,
            "name": application.name,
            "version": application.version,
            "status": application.status,
            "deployment_date": application.deployment_date
        }

@app.post("/applications", response_model=ApplicationResponse, status_code=201)
def create_application(application: ApplicationCreate):
    with Session(engine) as session:
        new_application = Application(
            name=application.name,
            version=application.version,
            status=application.status,
            deployment_date=application.deployment_date
        )

        session.add(new_application)
        session.commit()
        session.refresh(new_application)

        return new_application

@app.put(
    "/applications/{application_id}",
    response_model=ApplicationResponse
)
def update_application(
    application_id: int,
    application_data: ApplicationUpdate
):
    with Session(engine) as session:
        application = session.get(Application, application_id)

        if application is None:
            raise HTTPException(
                status_code=404,
                detail="Application not found"
            )

        application.name = application_data.name
        application.version = application_data.version
        application.status = application_data.status
        application.deployment_date = application_data.deployment_date

        session.commit()
        session.refresh(application)

        return application

@app.delete("/applications/{application_id}")
def delete_application(application_id: int):
    with Session(engine) as session:
        application = session.get(Application, application_id)

        if application is None:
            raise HTTPException(
                status_code=404,
                detail="Application not found"
            )

        session.delete(application)
        session.commit()

        return {
            "message": "Application deleted successfully"
        }