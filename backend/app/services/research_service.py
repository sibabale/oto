from datetime import date

from app.config import get_settings
from app.models.financials import CompanyResearchResponse, FinancialYear, ResearchScore


# Oldest→newest mock facts; fiscal years are assigned as [anchor-4, …, anchor].
_MOCK_FACTS_OLDEST_FIRST: list[dict[str, float]] = [
    {
        "revenue": 5_000_000_000,
        "gross_profit": 2_050_000_000,
        "operating_income": 700_000_000,
        "net_income": 450_000_000,
        "total_assets": 9_400_000_000,
        "total_liabilities": 3_200_000_000,
        "total_equity": 6_200_000_000,
        "total_debt": 1_450_000_000,
        "cash_and_equivalents": 950_000_000,
    },
    {
        "revenue": 5_350_000_000,
        "gross_profit": 2_210_000_000,
        "operating_income": 760_000_000,
        "net_income": 500_000_000,
        "total_assets": 9_800_000_000,
        "total_liabilities": 3_100_000_000,
        "total_equity": 6_700_000_000,
        "total_debt": 1_380_000_000,
        "cash_and_equivalents": 1_020_000_000,
    },
    {
        "revenue": 5_750_000_000,
        "gross_profit": 2_450_000_000,
        "operating_income": 840_000_000,
        "net_income": 560_000_000,
        "total_assets": 10_300_000_000,
        "total_liabilities": 3_100_000_000,
        "total_equity": 7_200_000_000,
        "total_debt": 1_300_000_000,
        "cash_and_equivalents": 1_090_000_000,
    },
    {
        "revenue": 6_050_000_000,
        "gross_profit": 2_680_000_000,
        "operating_income": 920_000_000,
        "net_income": 620_000_000,
        "total_assets": 10_700_000_000,
        "total_liabilities": 3_000_000_000,
        "total_equity": 7_700_000_000,
        "total_debt": 1_210_000_000,
        "cash_and_equivalents": 1_180_000_000,
    },
    {
        "revenue": 6_400_000_000,
        "gross_profit": 2_900_000_000,
        "operating_income": 1_010_000_000,
        "net_income": 680_000_000,
        "total_assets": 11_100_000_000,
        "total_liabilities": 2_900_000_000,
        "total_equity": 8_200_000_000,
        "total_debt": 1_140_000_000,
        "cash_and_equivalents": 1_260_000_000,
    },
]


def _rolling_mock_window(anchor_year: int) -> list[FinancialYear]:
    start = anchor_year - 4
    return [
        FinancialYear(fiscal_year=start + i, **_MOCK_FACTS_OLDEST_FIRST[i])
        for i in range(5)
    ]


def _build_response(
    ticker: str, company_name: str, history_oldest_first: list[FinancialYear]
) -> CompanyResearchResponse:
    if not history_oldest_first:
        raise ValueError("history_oldest_first must not be empty")

    latest = history_oldest_first[-1]
    debt_to_equity = (
        latest.total_liabilities / latest.total_equity if latest.total_equity else 0.0
    )
    net_margin = latest.net_income / latest.revenue if latest.revenue else 0.0
    first = history_oldest_first[0]
    revenue_growth = (
        (latest.revenue - first.revenue) / first.revenue if first.revenue else 0.0
    )

    profitability = round(min(100.0, max(0.0, net_margin * 400)), 2)
    strength = round(min(100.0, max(0.0, (1.0 - debt_to_equity) * 100)), 2)
    growth = round(min(100.0, max(0.0, revenue_growth * 100)), 2)
    valuation = 70.0
    total_score = round(
        profitability * 0.30 + strength * 0.30 + growth * 0.25 + valuation * 0.15,
        2,
    )

    return CompanyResearchResponse(
        ticker=ticker.upper(),
        company_name=company_name,
        years=list(reversed(history_oldest_first)),
        score=ResearchScore(
            total=total_score,
            profitability=profitability,
            strength=strength,
            growth=growth,
            valuation=valuation,
        ),
    )


def get_company_research(
    ticker: str, *, anchor_year: int | None = None
) -> CompanyResearchResponse:
    settings = get_settings()
    normalized = ticker.upper().strip()
    year = anchor_year if anchor_year is not None else date.today().year

    if settings.research_data_source.strip().lower() == "mock":
        history = _rolling_mock_window(year)
        return _build_response(
            normalized, f"{normalized} Incorporated", history
        )

    from app.services.sec_edgar import load_financial_history

    company_name, rows = load_financial_history(
        normalized, anchor_year=year, max_years=5
    )
    history = [
        FinancialYear(
            fiscal_year=int(r["fiscal_year"]),
            revenue=float(r["revenue"]),
            gross_profit=float(r["gross_profit"]),
            operating_income=float(r["operating_income"]),
            net_income=float(r["net_income"]),
            total_assets=float(r["total_assets"]),
            total_liabilities=float(r["total_liabilities"]),
            total_equity=float(r["total_equity"]),
            total_debt=float(r["total_debt"]),
            cash_and_equivalents=float(r["cash_and_equivalents"]),
        )
        for r in rows
    ]
    return _build_response(normalized, company_name, history)
