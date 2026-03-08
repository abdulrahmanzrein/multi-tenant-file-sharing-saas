from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user, require_admin
from app.models.tenant import Tenant
from app.models.user import User
from app.schemas.tenant import TenantCreate, TenantRead


router = APIRouter()


@router.post("/", response_model=TenantRead)
def create_tenant(tenant: TenantCreate, db: Session = Depends(get_db), user: User = Depends(require_admin)):
    """Create a new tenant"""

    db_tenant = Tenant(name=tenant.name, slug=tenant.slug)
    db.add(db_tenant)
    db.commit()
    db.refresh(db_tenant)

    return db_tenant


@router.get("/{tenant_id}", response_model=TenantRead)
def get_tenant(tenant_id: UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """Get tenant by ID"""
    if tenant_id != user.tenant_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()

    if tenant is None:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    return tenant


@router.get("/", response_model=list[TenantRead])
def list_tenants(db: Session = Depends(get_db), user: User = Depends(require_admin)):
    tenants = db.query(Tenant).all()
    return tenants

