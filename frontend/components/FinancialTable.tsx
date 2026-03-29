import type { FinancialYear } from "@/lib/types";

interface FinancialTableProps {
  rows: FinancialYear[];
}

export function FinancialTable({ rows }: FinancialTableProps): JSX.Element {
  return (
    <div className="overflow-x-auto rounded-lg border border-slate-200 bg-white">
      <table className="min-w-full text-left text-sm">
        <thead className="bg-slate-100 text-slate-600">
          <tr>
            <th className="px-4 py-3">Year</th>
            <th className="px-4 py-3">Revenue</th>
            <th className="px-4 py-3">Net Income</th>
            <th className="px-4 py-3">Total Assets</th>
            <th className="px-4 py-3">Total Liabilities</th>
            <th className="px-4 py-3">Equity</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.fiscal_year} className="border-t border-slate-200">
              <td className="px-4 py-3 font-medium text-slate-900">{row.fiscal_year}</td>
              <td className="px-4 py-3">{formatCurrency(row.revenue)}</td>
              <td className="px-4 py-3">{formatCurrency(row.net_income)}</td>
              <td className="px-4 py-3">{formatCurrency(row.total_assets)}</td>
              <td className="px-4 py-3">{formatCurrency(row.total_liabilities)}</td>
              <td className="px-4 py-3">{formatCurrency(row.total_equity)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function formatCurrency(value: number): string {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  }).format(value);
}
