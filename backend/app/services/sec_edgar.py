"""SEC EDGAR public APIs (no API key). See https://www.sec.gov/developer."""

from __future__ import annotations

import json
from functools import cache
from typing import Any

import httpx

from app.config import get_settings

COMPANY_TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
COMPANY_FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"

# Prefer ASC 606 revenue when present; fall back to older tags.
REVENUE_TAGS = (
    "RevenueFromContractWithCustomerExcludingAssessedTax",
    "Revenues",
    "SalesRevenueNet",
)

FY_TAGS = {
    "revenue": REVENUE_TAGS,
    "gross_profit": ("GrossProfit",),
    "operating_income": ("OperatingIncomeLoss",),
    "net_income": ("NetIncomeLoss",),
    "total_assets": ("Assets",),
    "total_liabilities": ("Liabilities",),
    "total_equity": ("StockholdersEquity",),
    "cash_and_equivalents": ("CashAndCashEquivalentsAtCarryingValue",),
}


class TickerNotFoundError(LookupError):
    """Ticker is not present in SEC company_tickers mapping."""


class EdgarUnavailableError(OSError):
    """Network or parse failure talking to SEC endpoints."""


def _client() -> httpx.Client:
    settings = get_settings()
    return httpx.Client(
        headers={
            "User-Agent": settings.sec_user_agent,
            "Accept-Encoding": "gzip, deflate",
        },
        timeout=30.0,
        follow_redirects=True,
    )


@cache
def _ticker_to_cik() -> dict[str, int]:
    with _client() as client:
        try:
            response = client.get(COMPANY_TICKERS_URL)
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise EdgarUnavailableError(
                "Could not load SEC ticker list."
            ) from exc
    raw: dict[str, Any] = response.json()
    out: dict[str, int] = {}
    for entry in raw.values():
        if not isinstance(entry, dict):
            continue
        sym = entry.get("ticker")
        cik = entry.get("cik_str")
        if isinstance(sym, str) and isinstance(cik, int):
            out[sym.upper()] = cik
    return out


def resolve_cik(ticker: str) -> int:
    normalized = ticker.upper().strip()
    mapping = _ticker_to_cik()
    if normalized not in mapping:
        raise TickerNotFoundError(normalized)
    return mapping[normalized]


def _cik_padded(cik: int) -> str:
    return f"{cik:010d}"


def fetch_company_facts_json(cik: int) -> dict[str, Any]:
    url = COMPANY_FACTS_URL.format(cik=_cik_padded(cik))
    with _client() as client:
        try:
            response = client.get(url)
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise EdgarUnavailableError(
                f"Could not load SEC company facts for CIK {cik}."
            ) from exc
    try:
        return json.loads(response.content)
    except json.JSONDecodeError as exc:
        raise EdgarUnavailableError("SEC company facts response was not JSON.") from exc


def _best_fy_row(rows: list[dict[str, Any]]) -> dict[str, Any] | None:
    candidates = [
        r
        for r in rows
        if r.get("fp") == "FY" and r.get("form") == "10-K" and r.get("fy") is not None
    ]
    if not candidates:
        return None
    return max(candidates, key=lambda r: str(r.get("filed", "")))


def _fy_value_usd(us_gaap: dict[str, Any], tag: str, fiscal_year: int) -> float | None:
    block = us_gaap.get(tag)
    if not isinstance(block, dict):
        return None
    units = block.get("units") or {}
    series = units.get("USD")
    if not series:
        for v in units.values():
            if isinstance(v, list):
                series = v
                break
    if not isinstance(series, list):
        return None
    rows = [r for r in series if r.get("fy") == fiscal_year]
    row = _best_fy_row(rows)
    if not row or "val" not in row:
        return None
    return float(row["val"])


def _first_tag_value(
    us_gaap: dict[str, Any], tags: tuple[str, ...], fiscal_year: int
) -> float | None:
    for tag in tags:
        val = _fy_value_usd(us_gaap, tag, fiscal_year)
        if val is not None:
            return val
    return None


def _total_debt(us_gaap: dict[str, Any], fiscal_year: int) -> float:
    lt = _fy_value_usd(us_gaap, "LongTermDebt", fiscal_year)
    cp = _fy_value_usd(us_gaap, "CommercialPaper", fiscal_year)
    parts = [x for x in (lt, cp) if x is not None]
    if parts:
        return float(sum(parts))
    alt = _fy_value_usd(us_gaap, "DebtInstrumentCarryingAmount", fiscal_year)
    return float(alt) if alt is not None else 0.0


def _available_fiscal_years(us_gaap: dict[str, Any]) -> set[int]:
    years: set[int] = set()
    for tag in REVENUE_TAGS:
        block = us_gaap.get(tag)
        if not isinstance(block, dict):
            continue
        for series in (block.get("units") or {}).values():
            if not isinstance(series, list):
                continue
            for row in series:
                if (
                    row.get("fp") == "FY"
                    and row.get("form") == "10-K"
                    and row.get("fy") is not None
                ):
                    years.add(int(row["fy"]))
    return years


def facts_to_financial_years(
    facts: dict[str, Any], *, anchor_year: int, max_years: int = 5
) -> tuple[str, list[dict[str, float | int]]]:
    """
    Returns (entity_name, rows oldest-first). Each row has fiscal_year + FinancialYear fields.
    """
    entity = str(facts.get("entityName") or "Unknown")
    us_gaap = facts.get("facts", {}).get("us-gaap")
    if not isinstance(us_gaap, dict):
        raise EdgarUnavailableError("SEC facts payload missing us-gaap.")

    pool = _available_fiscal_years(us_gaap)
    end = min(anchor_year, max(pool) if pool else anchor_year)
    wanted = [y for y in range(end, end - max_years, -1) if y in pool]
    wanted.sort()

    rows: list[dict[str, float | int]] = []
    for fy in wanted:
        revenue = _first_tag_value(us_gaap, REVENUE_TAGS, fy)
        if revenue is None:
            continue
        gross = _first_tag_value(us_gaap, FY_TAGS["gross_profit"], fy)
        op = _first_tag_value(us_gaap, FY_TAGS["operating_income"], fy)
        net = _first_tag_value(us_gaap, FY_TAGS["net_income"], fy)
        assets = _first_tag_value(us_gaap, FY_TAGS["total_assets"], fy)
        liab = _first_tag_value(us_gaap, FY_TAGS["total_liabilities"], fy)
        equity = _first_tag_value(us_gaap, FY_TAGS["total_equity"], fy)
        cash = _first_tag_value(us_gaap, FY_TAGS["cash_and_equivalents"], fy)

        rows.append(
            {
                "fiscal_year": fy,
                "revenue": max(0.0, revenue),
                "gross_profit": max(0.0, gross or 0.0),
                "operating_income": op if op is not None else 0.0,
                "net_income": net if net is not None else 0.0,
                "total_assets": max(0.0, assets or 0.0),
                "total_liabilities": max(0.0, liab or 0.0),
                "total_equity": equity if equity is not None else 0.0,
                "total_debt": max(0.0, _total_debt(us_gaap, fy)),
                "cash_and_equivalents": max(0.0, cash or 0.0),
            }
        )

    if not rows:
        raise EdgarUnavailableError(
            "No annual 10-K facts found for this issuer in SEC data."
        )

    return entity, rows


def load_financial_history(
    ticker: str, *, anchor_year: int, max_years: int = 5
) -> tuple[str, list[dict[str, float | int]]]:
    cik = resolve_cik(ticker)
    facts = fetch_company_facts_json(cik)
    return facts_to_financial_years(facts, anchor_year=anchor_year, max_years=max_years)
