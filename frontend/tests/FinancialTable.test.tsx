import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { FinancialTable } from "@/components/FinancialTable";

describe("FinancialTable", () => {
  it("renders yearly rows", () => {
    render(
      <FinancialTable
        rows={[
          {
            fiscal_year: 2024,
            revenue: 100,
            gross_profit: 50,
            operating_income: 20,
            net_income: 10,
            total_assets: 1,
            total_liabilities: 1,
            total_equity: 1,
            total_debt: 0.5,
            cash_and_equivalents: 0.2,
          },
          {
            fiscal_year: 2023,
            revenue: 90,
            gross_profit: 45,
            operating_income: 18,
            net_income: 9,
            total_assets: 1,
            total_liabilities: 1,
            total_equity: 1,
            total_debt: 0.5,
            cash_and_equivalents: 0.2,
          },
        ]}
      />,
    );

    expect(screen.getByText("2024")).toBeInTheDocument();
    expect(screen.getByText("$100")).toBeInTheDocument();
    expect(screen.getByText("$10")).toBeInTheDocument();
  });
});
