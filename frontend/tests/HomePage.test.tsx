import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import HomePage from "@/app/page";

vi.mock("@/lib/api", () => ({
  getFiveYearResearch: vi.fn().mockResolvedValue({
    ticker: "AAPL",
    company_name: "Apple Inc.",
    years: [
      {
        fiscal_year: 2024,
        revenue: 1000,
        gross_profit: 500,
        operating_income: 300,
        net_income: 200,
        total_assets: 3000,
        total_liabilities: 1200,
        total_equity: 1800,
        total_debt: 500,
        cash_and_equivalents: 600,
      },
      {
        fiscal_year: 2023,
        revenue: 900,
        gross_profit: 460,
        operating_income: 280,
        net_income: 190,
        total_assets: 2800,
        total_liabilities: 1150,
        total_equity: 1650,
        total_debt: 520,
        cash_and_equivalents: 590,
      },
      {
        fiscal_year: 2022,
        revenue: 850,
        gross_profit: 430,
        operating_income: 260,
        net_income: 180,
        total_assets: 2600,
        total_liabilities: 1100,
        total_equity: 1500,
        total_debt: 540,
        cash_and_equivalents: 560,
      },
      {
        fiscal_year: 2021,
        revenue: 800,
        gross_profit: 410,
        operating_income: 240,
        net_income: 160,
        total_assets: 2450,
        total_liabilities: 1050,
        total_equity: 1400,
        total_debt: 560,
        cash_and_equivalents: 540,
      },
      {
        fiscal_year: 2020,
        revenue: 760,
        gross_profit: 390,
        operating_income: 225,
        net_income: 150,
        total_assets: 2300,
        total_liabilities: 1000,
        total_equity: 1300,
        total_debt: 580,
        cash_and_equivalents: 520,
      },
    ],
    score: {
      total: 78,
      profitability: 80,
      strength: 75,
      growth: 70,
      valuation: 85,
    },
  }),
}));

describe("HomePage", () => {
  it("renders title and score card", async () => {
    render(await HomePage());

    expect(screen.getByText("OTO Research + Trade")).toBeInTheDocument();
    expect(screen.getByText("Sample Score")).toBeInTheDocument();
    expect(screen.getByText("78")).toBeInTheDocument();
  });
});
