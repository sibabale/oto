from __future__ import annotations

from pydantic import BaseModel, Field


class FinancialYear(BaseModel):
    fiscal_year: int = Field(..., ge=1900)
    revenue: float = Field(..., ge=0)
    gross_profit: float = Field(..., ge=0)
    operating_income: float
    net_income: float
    total_assets: float = Field(..., ge=0)
    total_liabilities: float = Field(..., ge=0)
    total_equity: float
    total_debt: float = Field(..., ge=0)
    cash_and_equivalents: float = Field(..., ge=0)


class ResearchScore(BaseModel):
    total: float = Field(..., ge=0, le=100)
    profitability: float = Field(..., ge=0, le=100)
    strength: float = Field(..., ge=0, le=100)
    growth: float = Field(..., ge=0, le=100)
    valuation: float = Field(..., ge=0, le=100)


class CompanyResearchResponse(BaseModel):
    ticker: str
    company_name: str
    years: list[FinancialYear]
    score: ResearchScore
