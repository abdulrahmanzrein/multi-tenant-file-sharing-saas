from fastapi import APIRouter

router = APIRouter()


@router.post("/")
def create_tenant():
    """Create a new tenant"""
    return {"message": "Create tenant - TODO"}


@router.get("/{tenant_id}")
def get_tenant(tenant_id: int):
    """Get tenant by ID"""
    return {"message": f"Get tenant {tenant_id} - TODO"}


@router.get("/")
def list_tenants():
    """List all tenants (admin only)"""
    return {"message": "List tenants - TODO"}
