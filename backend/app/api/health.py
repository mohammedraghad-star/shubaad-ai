from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status": "online",
        "platform": "SHUBAAD",
        "modules": {
            "spectral_engine": "ready",
            "gis_engine": "planned",
            "ai_engine": "planned"
        }
    }
