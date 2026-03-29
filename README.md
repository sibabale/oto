# OTO - Open Trading & Research MVP Starter

An open-source-friendly starter for:

- 5-year company research (income statement + balance sheet trends)
- simple scoring/ranking
- paper-trade order flow (stubbed endpoint ready for broker wiring)

## Stack

- Backend: FastAPI + Pydantic + Pytest
- Frontend: Next.js (App Router) + TypeScript + Tailwind + Vitest
- Data/Trading integrations (planned): SEC EDGAR CompanyFacts, Alpaca paper trading

## Project structure

```text
oto/
  backend/
    app/
    tests/
  frontend/
    app/
    components/
    lib/
    tests/
```

## Quick start

### 1) Backend

```bash
cd oto/backend
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload --port 8000
```

Run tests:

```bash
pytest
```

### 2) Frontend

```bash
cd oto/frontend
npm install
npm run dev
```

Run tests:

```bash
npm test
```

## Immediate next steps

1. Replace stub financial data with SEC CompanyFacts ingestion.
2. Wire `/api/v1/trades` to Alpaca paper endpoint.
3. Add auth + per-user portfolios.
4. Add persistence (Postgres + migrations).
