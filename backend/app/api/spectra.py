from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.spectral_engine import analyze_ftir_csv

router = APIRouter()

@router.post("/analyze")
async def analyze_spectrum(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported in v1.")

    content = await file.read()

    try:
        return analyze_ftir_csv(content)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))
