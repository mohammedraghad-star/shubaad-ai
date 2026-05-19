# SHUBAAD System Architecture v1

SHUBAAD is an AI-driven environmental intelligence platform for arid and semi-arid ecosystems. The platform integrates FTIR spectroscopy, soil chemistry, GIS layers, microbiome metadata, and machine-learning models to support salinity, drought, soil carbon, and resilience assessment.

## Core v1 modules

### 1. Spectral Engine
Input:
- FTIR CSV files
- Wavenumber column
- Absorbance/transmittance column
- Sample metadata

Processing:
- Validation
- Baseline correction
- Vector or max normalization
- Peak detection
- FTIR index extraction
- PCA-ready matrix preparation

Outputs:
- Cleaned spectrum
- Peak table
- Spectral indices
- JSON report

### 2. GIS Engine
Input:
- Sample coordinates
- Site metadata
- Sentinel/Landsat-derived indices
- Soil salinity and vegetation layers

Processing:
- Point-based sample mapping
- Raster summary extraction
- Spatial risk classification

Outputs:
- Site map
- Risk class
- GeoJSON layers

### 3. AI Decision Engine
Input:
- FTIR indices
- Soil EC/pH/OC/SOM
- NDVI/NDWI/LST
- Microbiome indicators

Models:
- PCA
- PLS regression
- Random Forest / Gradient Boosting
- Salinity risk classifier

Outputs:
- Salinity risk
- SOM degradation status
- Resilience score
- Model confidence

## Deployment model

Frontend:
- Next.js on Vercel

Backend:
- FastAPI on Render/Fly.io/Railway

Database:
- PostgreSQL + PostGIS on Supabase

Storage:
- Supabase Storage or S3-compatible bucket

## Scientific validation

Minimum validation standards:
- Replicated samples
- External validation dataset where possible
- Cross-validation for ML models
- RMSE, R², RPD for regression models
- Confusion matrix for classification models
- ANOVA/Tukey for treatment-based studies
