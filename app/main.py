from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.core.config import settings

from app.api.routers import chat, weather, hotels
from app.services.rag_service import rag_service
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Log and trigger data ingestion
    csv_path = os.path.join(os.getcwd(), "app/services", "cost_of_living_dataset.csv")
    
    # We offload it slightly so it doesn't block the server boot 
    rag_service.ingest_cost_of_living_data(csv_path)
    
    yield
    # Cleanup if needed

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
    description="Startup-Grade AI Travel Agent API"
)

# Set up Rate Limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Static Files and Templates for Frontend
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/")
async def serve_frontend(request: Request):
    """Serve the Vanilla SPA Web Application"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": settings.VERSION}

# We will include routers here once they are implemented
app.include_router(chat.router, prefix="/api/v1/chat", tags=["AI Chat"])
app.include_router(weather.router, prefix="/api/v1/weather", tags=["Weather"])
app.include_router(hotels.router, prefix="/api/v1/hotels", tags=["Hotels"])
