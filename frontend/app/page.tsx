import { FinancialTable } from "@/components/FinancialTable";
import { MetricCard } from "@/components/MetricCard";
import { getFiveYearResearch } from "@/lib/api";

const DEFAULT_TICKER = "AAPL";

export default async function HomePage() {
  const research = await getFiveYearResearch(DEFAULT_TICKER);
  const latest = research.years[0];

  return (
    <main className="mx-auto flex min-h-screen max-w-5xl flex-col gap-6 p-6">
      <header className="space-y-1">
        <h1 className="text-3xl font-bold tracking-tight">OTO Research + Trade</h1>
        <p className="text-slate-600">
          Starter dashboard for 5-year financial research and paper trading.
        </p>
      </header>

      <section className="grid grid-cols-1 gap-4 md:grid-cols-4">
        <MetricCard label="Ticker" value={research.ticker} />
        <MetricCard label="Latest Revenue" value={`$${latest.revenue.toLocaleString()}`} />
        <MetricCard
          label="Latest Net Income"
          value={`$${latest.net_income.toLocaleString()}`}
        />
        <MetricCard label="Sample Score" value={String(research.score.total)} />
      </section>

      <section className="rounded-lg border bg-white p-4 shadow-sm">
        <h2 className="mb-3 text-lg font-semibold">5-Year Snapshot</h2>
        <FinancialTable rows={research.years} />
      </section>
    </main>
  );
}
