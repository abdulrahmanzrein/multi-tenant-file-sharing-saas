from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api.v1.router import api_router
from app.core.limiter import limiter
from app.middleware.tenant_middleware import TenantMiddleware


app = FastAPI(
    title="File Sharing SaaS",
    description="A multi-tenant file sharing platform",
    version="1.0.0"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Include API router
app.add_middleware(TenantMiddleware)
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "File Sharing SaaS API", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
