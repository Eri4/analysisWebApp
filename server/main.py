from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# Import schemas first to initialize them properly
from app import schemas

# Then import routes
from app.api.routes import campaigns, analyses, recommendations
from app.core.config import settings
from app.core.scheduler import setup_scheduler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Global scheduler variable
scheduler = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize and start scheduler
    global scheduler
    scheduler = setup_scheduler()

    yield

    # Shutdown: clean up resources
    if scheduler:
        scheduler.shutdown()

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    campaigns.router,
    prefix=f"{settings.API_V1_STR}/campaigns",
    tags=["campaigns"],
)
app.include_router(
    analyses.router,
    prefix=f"{settings.API_V1_STR}/analyses",
    tags=["analyses"],
)
app.include_router(
    recommendations.router,
    prefix=f"{settings.API_V1_STR}/recommendations",
    tags=["recommendations"],
)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Marketing Analytics API",
        "docs_url": "/docs",
        "version": "0.1.0"
    }