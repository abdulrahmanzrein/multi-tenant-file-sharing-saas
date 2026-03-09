from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


def log_action(db: Session, user_id: UUID, tenant_id: UUID, action: str, resource_id: Optional[UUID] = None) -> None:
    audit_log = AuditLog(user_id=user_id, tenant_id=tenant_id, action=action, resource_id=resource_id)
    db.add(audit_log)

