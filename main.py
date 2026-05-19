from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import spectra, health

app = FastAPI(
    title="SHUBAAD Scientific API",
    version="1.0.0",
    description="Backend API for FTIR, GIS, and AI-driven environmental resilience analysis."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api")
app.include_router(spectra.router, prefix="/api/spectra")
