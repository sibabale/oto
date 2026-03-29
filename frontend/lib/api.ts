import type { CompanyResearchResponse, TradeRequest, TradeResponse } from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export async function getFiveYearResearch(
  ticker: string,
): Promise<CompanyResearchResponse> {
  const res = await fetch(`${API_BASE_URL}/api/v1/research/${ticker}`, {
    method: "GET",
    cache: "no-store",
  });

  if (!res.ok) {
    throw new Error(`Failed to load company research (${res.status})`);
  }

  return (await res.json()) as CompanyResearchResponse;
}

export async function submitTrade(payload: TradeRequest): Promise<TradeResponse> {
  const res = await fetch(`${API_BASE_URL}/api/v1/trades`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      ticker: payload.ticker,
      side: payload.side,
      order_type: payload.order_type,
      quantity: payload.quantity,
      limit_price: payload.limit_price,
    }),
  });

  if (!res.ok) {
    throw new Error(`Failed to submit trade (${res.status})`);
  }

  return (await res.json()) as TradeResponse;
}
