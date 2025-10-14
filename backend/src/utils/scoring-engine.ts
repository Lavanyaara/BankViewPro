import { Institution, HistoricalRecord, CategoryScores, MetricConfig } from '../../../shared/interfaces';

const CATEGORY_WEIGHTS = {
  capitalization: 0.25,
  asset_quality: 0.30,
  profitability: 0.25,
  liquidity: 0.20
};

function scoreMetric(value: number, config: MetricConfig): number {
  const { excellent, good, fair, poor, reverse = false } = config;

  if (reverse) {
    // Lower values are better
    if (value <= excellent) return 10;
    if (value <= good) return 7 + 3 * (good - value) / (good - excellent);
    if (value <= fair) return 5 + 2 * (fair - value) / (fair - good);
    if (value <= poor) return 2 + 3 * (poor - value) / (poor - fair);
    return 1;
  } else {
    // Higher values are better
    if (value >= excellent) return 10;
    if (value >= good) return 7 + 3 * (value - good) / (excellent - good);
    if (value >= fair) return 5 + 2 * (value - fair) / (good - fair);
    if (value >= poor) return 2 + 3 * (value - poor) / (fair - poor);
    return poor > 0 ? 1 + (value / poor) : 1;
  }
}

export function calculateCapitalizationScore(data: HistoricalRecord): number {
  const metricsConfig: Record<string, MetricConfig> = {
    capital_adequacy_ratio: { weight: 0.35, excellent: 15, good: 12, fair: 10, poor: 8 },
    tier1_ratio: { weight: 0.35, excellent: 12, good: 10, fair: 8, poor: 6 },
    leverage_ratio: { weight: 0.30, excellent: 8, good: 6, fair: 5, poor: 3 }
  };

  let totalScore = 0;
  for (const [metric, config] of Object.entries(metricsConfig)) {
    const value = data[metric as keyof HistoricalRecord] as number;
    const metricScore = scoreMetric(value, config);
    totalScore += metricScore * config.weight;
  }

  return Math.min(10.0, Math.max(1.0, totalScore));
}

export function calculateAssetQualityScore(data: HistoricalRecord): number {
  const metricsConfig: Record<string, MetricConfig> = {
    npl_ratio: { weight: 0.40, excellent: 0.5, good: 1.0, fair: 2.0, poor: 3.0, reverse: true },
    loan_loss_provisions: { weight: 0.30, excellent: 0.3, good: 0.5, fair: 1.0, poor: 1.5, reverse: true },
    coverage_ratio: { weight: 0.20, excellent: 120, good: 100, fair: 80, poor: 60 },
    asset_classification: { weight: 0.10, excellent: 1, good: 2, fair: 4, poor: 6, reverse: true }
  };

  let totalScore = 0;
  for (const [metric, config] of Object.entries(metricsConfig)) {
    const value = data[metric as keyof HistoricalRecord] as number;
    const metricScore = scoreMetric(value, config);
    totalScore += metricScore * config.weight;
  }

  return Math.min(10.0, Math.max(1.0, totalScore));
}

export function calculateProfitabilityScore(data: HistoricalRecord): number {
  const metricsConfig: Record<string, MetricConfig> = {
    return_on_assets: { weight: 0.25, excellent: 1.5, good: 1.2, fair: 0.8, poor: 0.4 },
    return_on_equity: { weight: 0.25, excellent: 15, good: 12, fair: 8, poor: 4 },
    net_interest_margin: { weight: 0.25, excellent: 4.0, good: 3.5, fair: 2.5, poor: 1.5 },
    cost_to_income_ratio: { weight: 0.15, excellent: 50, good: 60, fair: 70, poor: 80, reverse: true },
    earnings_per_share: { weight: 0.10, excellent: 10, good: 8, fair: 5, poor: 2 }
  };

  let totalScore = 0;
  for (const [metric, config] of Object.entries(metricsConfig)) {
    const value = data[metric as keyof HistoricalRecord] as number;
    const metricScore = scoreMetric(value, config);
    totalScore += metricScore * config.weight;
  }

  return Math.min(10.0, Math.max(1.0, totalScore));
}

export function calculateLiquidityScore(data: HistoricalRecord): number {
  const metricsConfig: Record<string, MetricConfig> = {
    liquidity_coverage_ratio: { weight: 0.35, excellent: 130, good: 115, fair: 105, poor: 100 },
    net_stable_funding_ratio: { weight: 0.35, excellent: 115, good: 110, fair: 105, poor: 100 },
    loan_to_deposit_ratio: { weight: 0.20, excellent: 70, good: 80, fair: 90, poor: 100, reverse: true },
    cash_ratio: { weight: 0.10, excellent: 15, good: 12, fair: 8, poor: 5 }
  };

  let totalScore = 0;
  for (const [metric, config] of Object.entries(metricsConfig)) {
    const value = data[metric as keyof HistoricalRecord] as number;
    const metricScore = scoreMetric(value, config);
    totalScore += metricScore * config.weight;
  }

  return Math.min(10.0, Math.max(1.0, totalScore));
}

export function calculateOverallScore(institution: Institution): CategoryScores {
  const latestData = institution.historical_data[institution.historical_data.length - 1];

  const capitalization = calculateCapitalizationScore(latestData);
  const asset_quality = calculateAssetQualityScore(latestData);
  const profitability = calculateProfitabilityScore(latestData);
  const liquidity = calculateLiquidityScore(latestData);

  const overall = 
    capitalization * CATEGORY_WEIGHTS.capitalization +
    asset_quality * CATEGORY_WEIGHTS.asset_quality +
    profitability * CATEGORY_WEIGHTS.profitability +
    liquidity * CATEGORY_WEIGHTS.liquidity;

  return {
    capitalization,
    asset_quality,
    profitability,
    liquidity,
    overall: Math.min(10.0, Math.max(1.0, overall))
  };
}

export function getRatingLabel(score: number): string {
  if (score >= 8.5) return 'Excellent';
  if (score >= 7.0) return 'Very Good';
  if (score >= 5.5) return 'Good';
  if (score >= 4.0) return 'Fair';
  return 'Poor';
}
