import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.api.routes import router

# Rate limiter setup
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Reliable Researcher API",
    version="1.0.0",
    description="Production-grade Agentic RAG application for reliable research"
)

# Add rate limiter to app state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Environment-based CORS configuration
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Configure CORS
allowed_origins = ["*"] if ENVIRONMENT == "development" else [FRONTEND_URL]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api")

# Health check endpoint
@app.get("/health")
@limiter.limit("30/minute")
async def health_check(request: Request):
    """Health check endpoint for monitoring and Railway deployment"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "environment": ENVIRONMENT
    }

# Serve static frontend files in production
if ENVIRONMENT == "production" and os.path.exists("frontend/dist"):
    app.mount("/assets", StaticFiles(directory="frontend/dist/assets"), name="assets")

    @app.get("/")
    async def serve_root():
        """Serve index.html at root"""
        return FileResponse("frontend/dist/index.html")
    
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        """Serve frontend for all non-API routes"""
        file_path = f"frontend/dist/{full_path}"
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse("frontend/dist/index.html")
else:
    @app.get("/")
    def read_root():
        return {
            "message": "Reliable Researcher API is running.",
            "docs": "/docs",
            "health": "/health"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
