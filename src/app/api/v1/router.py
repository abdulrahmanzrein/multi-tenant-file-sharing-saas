from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, tenants, files

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(tenants.router, prefix="/tenants", tags=["tenants"])
api_router.include_router(files.router, prefix="/files", tags=["files"])
