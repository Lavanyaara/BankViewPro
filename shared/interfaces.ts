export interface HistoricalRecord {
  year: number;
  capital_adequacy_ratio: number;
  tier1_ratio: number;
  leverage_ratio: number;
  risk_weighted_assets: number;
  npl_ratio: number;
  loan_loss_provisions: number;
  coverage_ratio: number;
  asset_classification: number;
  return_on_assets: number;
  return_on_equity: number;
  net_interest_margin: number;
  cost_to_income_ratio: number;
  earnings_per_share: number;
  liquidity_coverage_ratio: number;
  net_stable_funding_ratio: number;
  loan_to_deposit_ratio: number;
  cash_ratio: number;
}

export interface Institution {
  institution_name: string;
  institution_type: 'Bank' | 'Broker Dealer';
  assets: number;
  employees: number;
  branches: number;
  historical_data: HistoricalRecord[];
}

export interface CategoryScores {
  capitalization: number;
  asset_quality: number;
  profitability: number;
  liquidity: number;
  overall: number;
}

export interface MetricBenchmark {
  excellent: number;
  good: number;
  fair: number;
  poor: number;
}

export interface MetricConfig extends MetricBenchmark {
  weight: number;
  reverse?: boolean;
}

export interface MetricInfo {
  name: string;
  unit: string;
  description: string;
  benchmark: MetricBenchmark;
}

export interface CategoryMetricInfo {
  [key: string]: MetricInfo;
}

export interface AllMetricInfo {
  capitalization: CategoryMetricInfo;
  asset_quality: CategoryMetricInfo;
  profitability: CategoryMetricInfo;
  liquidity: CategoryMetricInfo;
}
