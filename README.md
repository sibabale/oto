# OTO - Open Trading & Research MVP Starter

An open-source-friendly starter for:

- 5-year company research (income statement + balance sheet trends)
- simple scoring/ranking
- paper-trade order flow (stubbed endpoint ready for broker wiring)

## Stack

- Backend: FastAPI + Pydantic + Pytest
- Frontend: Next.js (App Router) + TypeScript + Tailwind + Vitest
- Data: SEC EDGAR CompanyFacts (free, official; set `OTO_SEC_USER_AGENT` with a real contact email)
- Trading integrations (planned): Alpaca paper trading

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

**SEC EDGAR (real company data):** The SEC expects a descriptive `User-Agent` including contact information. Example:

```bash
export OTO_SEC_USER_AGENT="YourApp/1.0 (your@email.com)"
export OTO_RESEARCH_DATA_SOURCE=sec
```

Use `OTO_RESEARCH_DATA_SOURCE=mock` for offline or CI (tests default to mock via `tests/conftest.py`).

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

1. ~~Replace stub financial data with SEC CompanyFacts ingestion.~~ (Done: `GET /api/v1/research/{ticker}` uses SEC when `OTO_RESEARCH_DATA_SOURCE=sec`, default in production code. Tests use `OTO_RESEARCH_DATA_SOURCE=mock`.)
2. Wire `/api/v1/trades` to Alpaca paper endpoint.
3. Add auth + per-user portfolios.
4. Add persistence (Postgres + migrations).
