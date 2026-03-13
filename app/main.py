from fastapi import FastAPI
from sqlmodel import Session, select

from app.db import engine, init_db
from app.models.service import Service
from app.models.tenant import Tenant
from app.models.user import User, UserRole
from app.routes import appointments, auth, availability, messages, notifications, progress, services, slots, users

app = FastAPI(title="Driving School SaaS Backend")


@app.on_event("startup")
def on_startup() -> None:
    init_db()
    seed_initial_data()


def seed_initial_data() -> None:
    with Session(engine) as session:
        tenant = session.exec(select(Tenant).where(Tenant.id == 1)).first()
        if not tenant:
            tenant = Tenant(id=1, name="Auto-école Démo")
            session.add(tenant)
            session.commit()
            session.refresh(tenant)

        owner = session.exec(select(User).where(User.email == "owner@demo.local", User.tenant_id == tenant.id)).first()
        if not owner:
            session.add(User(tenant_id=tenant.id, name="Owner Demo", email="owner@demo.local", role=UserRole.owner))

        instructor = session.exec(select(User).where(User.email == "instructor@demo.local", User.tenant_id == tenant.id)).first()
        if not instructor:
            session.add(
                User(tenant_id=tenant.id, name="Moniteur Demo", email="instructor@demo.local", role=UserRole.instructor)
            )

        student = session.exec(select(User).where(User.email == "student@demo.local", User.tenant_id == tenant.id)).first()
        if not student:
            session.add(User(tenant_id=tenant.id, name="Élève Demo", email="student@demo.local", role=UserRole.student))

        existing_services = session.exec(select(Service).where(Service.tenant_id == tenant.id)).all()
        if not existing_services:
            session.add(Service(tenant_id=tenant.id, name="Conduite - Boîte manuelle", duration_minutes=60))
            session.add(Service(tenant_id=tenant.id, name="Conduite - Boîte auto", duration_minutes=60))

        session.commit()


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(services.router)
app.include_router(slots.router)
app.include_router(appointments.router)
app.include_router(progress.router)
app.include_router(messages.router)
app.include_router(notifications.router)
app.include_router(availability.router)


@app.get("/", tags=["health"])
def read_root() -> dict[str, str]:
    return {"message": "Driving School SaaS Backend is running"}
