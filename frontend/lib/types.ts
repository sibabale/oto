export interface FinancialYear {
  fiscal_year: number;
  revenue: number;
  gross_profit: number;
  operating_income: number;
  net_income: number;
  total_assets: number;
  total_liabilities: number;
  total_equity: number;
  total_debt: number;
  cash_and_equivalents: number;
}

export interface ResearchScore {
  total: number;
  profitability: number;
  strength: number;
  growth: number;
  valuation: number;
}

export interface CompanyResearchResponse {
  ticker: string;
  company_name: string;
  years: FinancialYear[];
  score: ResearchScore;
}

export interface TradeRequest {
  ticker: string;
  side: "buy" | "sell";
  order_type: "market" | "limit";
  qty: number;
  limit_price?: number;
}

export interface TradeResponse {
  order_id: string;
  status: "accepted" | "rejected";
  broker: string;
  ticker: string;
  side: "buy" | "sell";
  order_type: "market" | "limit";
  quantity: number;
  limit_price?: number | null;
  submitted_at: string;
}
