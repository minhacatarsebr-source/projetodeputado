# Electoral Heatmap - Deputado Federal SP 2026

Web application for optimizing Meta Ads campaign budget allocation based on historical electoral performance (TSE data).

## Features

- **Heatmap**: Visualize SP municipalities by electoral potential
- **Dashboard**: Table with municipality scores and recommendations
- **API**: REST endpoints for data retrieval and recommendations
- **Meta Integration**: Real-time campaign performance data
- **TSE Data**: Historical election results (2022, 2018)

## Architecture

```
Frontend (React/Vite)          Backend (FastAPI)              Database (PostgreSQL)
├─ Dashboard                    ├─ /api/municipalities        ├─ municipalities
├─ Heatmap                      ├─ /api/metrics               ├─ tse_votes_2022
├─ Tables                       ├─ /api/recommendations      ├─ tse_votes_2018
└─ Charts                       └─ /api/sync                 └─ meta_campaign_insights
```

## Setup

### Prerequisites

- Docker & Docker Compose
- Python 3.11+
- Node.js 18+
- Meta Ads API credentials

### 1. Database Setup

```bash
# Start PostgreSQL with PostGIS
docker-compose up -d postgres

# Wait for DB to be ready
sleep 10
```

### 2. Backend Setup

```bash
cd backend

# Create .env file
cp .env.example .env

# Update .env with your Meta credentials
# META_ACCESS_TOKEN=your_token
# META_AD_ACCOUNT_ID=your_account_id

# Install dependencies
pip install -r requirements.txt

# Import municipalities
python scripts/import_municipalities.py

# Import TSE data (after placing CSV files in data/ directory)
python scripts/import_tse_data.py

# Start API
python app.py
# API runs on http://localhost:8000
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env
cp .env.example .env

# Start dev server
npm run dev
# UI runs on http://localhost:5173
```

## Data Import

### TSE Electoral Data

1. Download 2022 & 2018 federal deputy results from [TSE](https://www.tse.jus.br/eleitor/glossario/termos/repositorio-de-dados-eleitorais)
2. Filter for São Paulo (UF = "SP")
3. Save as CSV files:
   - `data/tse_2022_sp_deputados.csv`
   - `data/tse_2018_sp_deputados.csv`
4. Expected columns: `UF, MUNICIPIO, CODIGO_MUNICIPIO, NM_CANDIDATO, QT_VOTOS`

### Meta Ads Data

The API automatically fetches campaign data from Meta Ads Graph API:

```bash
# Manually trigger sync
curl -X POST http://localhost:8000/api/sync
```

## API Endpoints

### Get All Municipalities
```bash
GET /api/municipalities?sort_by=potencial
```

### Get Municipality Details
```bash
GET /api/metrics/{municipality_id}
```

### Get Budget Recommendations
```bash
GET /api/recommendations
```

### Sync Meta Data
```bash
POST /api/sync
```

## Scoring Logic

### Potencial Score
- Based on historical electoral performance
- Formula: `(votes_2022 / total_votes) * 100 + growth_factor`
- Range: 0-100+

### Eficiência Score
- Based on current campaign performance
- Formula: `(ROAS / CPA_avg) * 10`
- Range: 0-10+

### Recommendations
- **INVEST_MORE**: High potential + High efficiency
- **TEST**: High potential + Low efficiency
- **MAINTAIN**: Low potential + High efficiency
- **REDUCE**: Low potential + Low efficiency

## Directory Structure

```
eleitoral_sp/
├── backend/
│   ├── app.py                    # FastAPI main
│   ├── database.py              # DB connection
│   ├── models.py                # SQLAlchemy models
│   ├── schemas.py               # Pydantic schemas
│   ├── routes/
│   │   └── municipalities.py    # API endpoints
│   ├── services/
│   │   ├── scoring.py           # Scoring logic
│   │   └── meta_fetch.py        # Meta API integration
│   ├── scripts/
│   │   ├── import_municipalities.py
│   │   └── import_tse_data.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   ├── components/
│   │   └── api/
│   └── package.json
├── data/
│   ├── tse_2022_sp_deputados.csv
│   └── tse_2018_sp_deputados.csv
├── docker-compose.yml
├── init.sql
└── README.md
```

## Next Steps

1. Place TSE CSV files in `data/` directory
2. Configure Meta Ads credentials in backend `.env`
3. Import municipalities and TSE data
4. Start backend and frontend
5. Access dashboard at http://localhost:5173

## Testing

```bash
# Test API health
curl http://localhost:8000/api/health

# Test get municipalities
curl http://localhost:8000/api/municipalities

# Test recommendations
curl http://localhost:8000/api/recommendations
```

## Deployment

Backend: Railway, Render, or Heroku
Frontend: Vercel, Netlify

Environment variables required:
- `DATABASE_URL`
- `META_ACCESS_TOKEN`
- `META_AD_ACCOUNT_ID`

## Voter Data Pipeline

Pipeline to clean voter Excel database, import to Kommo CRM, and upload to Meta as a Custom Audience for lookalike targeting.

### Run the full pipeline
```bash
python backend/scripts/run_voter_pipeline.py --input data/voters.xlsx
```

### Run individual steps
```bash
# Only clean
python backend/scripts/clean_voter_data.py --input data/voters.xlsx --output data/voters_clean.csv

# Only Kommo import (needs clean CSV)
python backend/scripts/import_to_kommo.py --input data/voters_clean.csv

# Only Meta upload (needs clean CSV)
python backend/scripts/upload_meta_audience.py --input data/voters_clean.csv
```

### Skip steps (e.g., only clean + Kommo, skip Meta)
```bash
python backend/scripts/run_voter_pipeline.py --input data/voters.xlsx --skip-meta
```

### After Meta upload: create Lookalike Audience
1. Meta Ads Manager → Públicos → "Eleitores Base 2022" → Criar Público Similar
2. País: Brasil, tamanhos: 1% / 2% / 3% (create all three simultaneously)
3. Aguardar 24-48h para o Meta processar

### Required .env variables
```
META_ACCESS_TOKEN=...
META_AD_ACCOUNT_ID=act_...
META_AUDIENCE_NAME=Eleitores Base 2022
KOMMO_SUBDOMAIN=...
KOMMO_TOKEN=...
```
