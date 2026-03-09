"""
Seed script — creates sample tenants and users for local development/demo.
Run from the project root: python scripts/seed.py
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from app.db.session import SessionLocal
from app.models.tenant import Tenant
from app.models.user import User
from app.core.security import get_password_hash


def seed():
    db = SessionLocal()
    try:
        # Tenant 1
        t1 = Tenant(name="Acme Corp", slug="acme")
        db.add(t1)
        db.commit()
        db.refresh(t1)

        db.add(User(
            email="admin@acme.com",
            hashed_password=get_password_hash("password123"),
            full_name="Acme Admin",
            role="admin",
            tenant_id=t1.id,
        ))
        db.add(User(
            email="member@acme.com",
            hashed_password=get_password_hash("password123"),
            full_name="Acme Member",
            role="member",
            tenant_id=t1.id,
        ))

        # Tenant 2
        t2 = Tenant(name="Globex Inc", slug="globex")
        db.add(t2)
        db.commit()
        db.refresh(t2)

        db.add(User(
            email="admin@globex.com",
            hashed_password=get_password_hash("password123"),
            full_name="Globex Admin",
            role="admin",
            tenant_id=t2.id,
        ))
        db.add(User(
            email="member@globex.com",
            hashed_password=get_password_hash("password123"),
            full_name="Globex Member",
            role="member",
            tenant_id=t2.id,
        ))

        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed()
    print("Seeding complete.")
