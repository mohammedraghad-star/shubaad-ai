CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    description TEXT,
    study_region TEXT,
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS samples (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    sample_code TEXT NOT NULL,
    sample_type TEXT,
    treatment TEXT,
    depth_cm TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    geom GEOGRAPHY(Point, 4326),
    collection_date DATE,
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS soil_metadata (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sample_id UUID REFERENCES samples(id) ON DELETE CASCADE,
    ec_ds_m DOUBLE PRECISION,
    ph DOUBLE PRECISION,
    oc_percent DOUBLE PRECISION,
    som_percent DOUBLE PRECISION,
    texture_class TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS ftir_spectra (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sample_id UUID REFERENCES samples(id) ON DELETE CASCADE,
    filename TEXT,
    wavenumber DOUBLE PRECISION[],
    absorbance DOUBLE PRECISION[],
    preprocessing_method TEXT,
    instrument TEXT,
    resolution_cm INTEGER,
    scans INTEGER,
    uploaded_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS analysis_outputs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sample_id UUID REFERENCES samples(id) ON DELETE CASCADE,
    analysis_type TEXT,
    result_json JSONB,
    figure_url TEXT,
    created_at TIMESTAMP DEFAULT now()
);
