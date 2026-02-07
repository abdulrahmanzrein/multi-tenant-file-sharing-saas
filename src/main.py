from fastapi import FastAPI
from app.api.v1.router import api_router

app = FastAPI(
    title="File Sharing SaaS",
    description="A multi-tenant file sharing platform",
    version="1.0.0"
)

# Include API router
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "File Sharing SaaS API", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
