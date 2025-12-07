from fastapi import FastAPI
from sqlmodel import select

from app.db import get_session, init_db
from app.models.service import Service
from app.models.tenant import Tenant
from app.models.user import User
from app.routes import appointments, availability, services

app = FastAPI(title="Appointment App Backend")


@app.on_event("startup")
def on_startup() -> None:
    init_db()
    seed_initial_data()


def seed_initial_data() -> None:
    with get_session() as session:
        tenant = session.exec(select(Tenant).where(Tenant.id == 1)).first()
        if not tenant:
            tenant = Tenant(id=1, name="Default Tenant")
            session.add(tenant)
            session.commit()
            session.refresh(tenant)

        default_user = session.exec(select(User).where(User.tenant_id == tenant.id)).first()
        if not default_user:
            user = User(tenant_id=tenant.id, name="Default User")
            session.add(user)

        existing_services = session.exec(select(Service).where(Service.tenant_id == tenant.id)).all()
        if not existing_services:
            session.add(Service(tenant_id=tenant.id, name="Consultation", duration_minutes=30))
            session.add(Service(tenant_id=tenant.id, name="Follow-up", duration_minutes=20))

        session.commit()


app.include_router(services.router)
app.include_router(appointments.router)
app.include_router(availability.router)


@app.get("/", tags=["health"])
def read_root() -> dict[str, str]:
    return {"message": "Appointment App Backend is running"}
