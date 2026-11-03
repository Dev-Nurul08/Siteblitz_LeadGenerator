# SiteBlitz Lead Intelligence OS

Internal sales intelligence and customer acquisition platform for web/mobile development agencies.

## Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 16+
- Redis 7+
- Node.js 20+ (for frontend)

### Backend Setup
```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -e ".[dev]"

# Configure environment
copy .env.example .env
# Edit .env with your database credentials

# Run migrations
alembic upgrade head

# Start API server
uvicorn backend.app.main:app --reload --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Architecture
See [Project Blueprint](docs/architecture.md) for full architecture documentation.

## Phase Status
- **Phase 1**: Discovery Engine — 🔄 In Progress
- **Phase 2**: Opportunity Engine — ⏳ Pending Phase 1 Approval
- **Phase 3**: Enrichment Engine — ⏳ Pending Phase 2 Approval
- **Phase 4**: Qualification Engine — ⏳ Pending Phase 3 Approval
- **Phase 5**: Conversion Engine — ⏳ Pending Phase 4 Approval
