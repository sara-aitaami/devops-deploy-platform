import logging
from typing import List

from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy import select
from sqlalchemy import text
from sqlalchemy.orm import Session

from .database import engine
from .models import Application
from .schemas import (
    ApplicationCreate,
    ApplicationResponse,
    ApplicationUpdate,
)

logger = logging.getLogger("devops-api")

app = FastAPI(title="DevOps Deploy Platform API")

Instrumentator().instrument(app).expose(app)

@app.get("/health")
def health():
    logger.info("Health check OK")
    return {"status": "ok"}


@app.get("/ready")
def ready():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        logger.info("Readiness check OK - database available")
        return {"status": "ready"}

    except Exception as exc:
        logger.error(
            "Readiness check failed - database unavailable",
            exc_info=True,
        )
        raise HTTPException(
            status_code=503,
            detail="Database is not ready",
        ) from exc

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
            logger.warning(
                "Application not found - application_id=%s",
                application_id,
            )
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
