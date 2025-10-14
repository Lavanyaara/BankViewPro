import { Institution, HistoricalRecord, AllMetricInfo } from '../../../shared/interfaces';

function seededRandom(seed: number): () => number {
  let value = seed;
  return () => {
    value = (value * 9301 + 49297) % 233280;
    return value / 233280;
  };
}

function hashString(str: string): number {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash;
  }
  return Math.abs(hash);
}

function normalRandom(mean: number, stdDev: number, rand: () => number): number {
  const u1 = rand();
  const u2 = rand();
  const z0 = Math.sqrt(-2.0 * Math.log(u1)) * Math.cos(2.0 * Math.PI * u2);
  return mean + z0 * stdDev;
}

export function generateSampleData(): Record<string, Institution> {
  const institutions = [
    "JPMorgan Chase & Co.",
    "Bank of America Corporation",
    "Wells Fargo & Company",
    "Citigroup Inc.",
    "Goldman Sachs Group Inc.",
    "Morgan Stanley",
    "U.S. Bancorp",
    "Truist Financial Corporation",
    "PNC Financial Services Group",
    "Charles Schwab Corporation"
  ];

  const currentYear = new Date().getFullYear();
  const years = Array.from({ length: 5 }, (_, i) => currentYear - 4 + i);

  const bankData: Record<string, Institution> = {};

  for (const institution of institutions) {
    const seed = hashString(institution);
    const rand = seededRandom(seed);

    const baseCar = rand() * (18 - 12) + 12;
    const baseTier1 = rand() * (15 - 10) + 10;
    const baseLeverage = rand() * (12 - 8) + 8;
    const baseRwa = rand() * (2000000 - 800000) + 800000;

    const baseNpl = rand() * (2.5 - 0.5) + 0.5;
    const baseProvisions = rand() * (1.2 - 0.3) + 0.3;
    const baseCoverage = rand() * (120 - 60) + 60;
    const baseClassification = rand() * (8 - 2) + 2;

    const baseRoa = rand() * (1.5 - 0.8) + 0.8;
    const baseRoe = rand() * (15 - 8) + 8;
    const baseNim = rand() * (4.0 - 2.5) + 2.5;
    const baseCostIncome = rand() * (75 - 55) + 55;
    const baseEps = rand() * (12 - 4) + 4;

    const baseLcr = rand() * (150 - 110) + 110;
    const baseNsfr = rand() * (130 - 105) + 105;
    const baseLtd = rand() * (90 - 70) + 70;
    const baseCash = rand() * (15 - 8) + 8;

    const yearlyData: HistoricalRecord[] = [];

    for (let i = 0; i < years.length; i++) {
      const year = years[i];
      const trendFactor = 1 + (i * 0.02 + normalRandom(0, 0.05, rand));
      const volatility = normalRandom(1, 0.08, rand);

      const record: HistoricalRecord = {
        year,
        capital_adequacy_ratio: Math.max(8, baseCar * trendFactor * volatility),
        tier1_ratio: Math.max(6, baseTier1 * trendFactor * volatility),
        leverage_ratio: Math.max(3, baseLeverage * trendFactor * volatility),
        risk_weighted_assets: baseRwa * (1 + i * 0.1) * volatility,
        npl_ratio: Math.max(0.1, baseNpl * (1 - i * 0.05) * volatility),
        loan_loss_provisions: Math.max(0.1, baseProvisions * (1 - i * 0.03) * volatility),
        coverage_ratio: baseCoverage * trendFactor * volatility,
        asset_classification: Math.max(1, baseClassification * (1 - i * 0.1) * volatility),
        return_on_assets: Math.max(0.1, baseRoa * trendFactor * volatility),
        return_on_equity: Math.max(2, baseRoe * trendFactor * volatility),
        net_interest_margin: Math.max(1, baseNim * trendFactor * volatility),
        cost_to_income_ratio: Math.max(40, Math.min(90, baseCostIncome * (1 - i * 0.02) * volatility)),
        earnings_per_share: Math.max(1, baseEps * trendFactor * volatility),
        liquidity_coverage_ratio: Math.max(100, baseLcr * trendFactor * volatility),
        net_stable_funding_ratio: Math.max(100, baseNsfr * trendFactor * volatility),
        loan_to_deposit_ratio: Math.max(50, Math.min(100, baseLtd * volatility)),
        cash_ratio: Math.max(3, baseCash * trendFactor * volatility)
      };

      yearlyData.push(record);
    }

    const institutionData: Institution = {
      institution_name: institution,
      institution_type: institution.includes('Bank') ? 'Bank' : 'Broker Dealer',
      assets: baseRwa * (rand() * (8 - 3) + 3),
      employees: Math.floor(rand() * (250000 - 50000) + 50000),
      branches: institution.includes('Bank') 
        ? Math.floor(rand() * (5000 - 1000) + 1000)
        : Math.floor(rand() * (500 - 100) + 100),
      historical_data: yearlyData
    };

    bankData[institution] = institutionData;
  }

  return bankData;
}

export function getMetricInfo(): AllMetricInfo {
  return {
    capitalization: {
      capital_adequacy_ratio: {
        name: 'Capital Adequacy Ratio',
        unit: '%',
        description: 'Measures bank\'s available capital as percentage of risk-weighted assets',
        benchmark: { excellent: 15, good: 12, fair: 10, poor: 8 }
      },
      tier1_ratio: {
        name: 'Tier 1 Capital Ratio',
        unit: '%',
        description: 'Core capital ratio measuring financial strength',
        benchmark: { excellent: 12, good: 10, fair: 8, poor: 6 }
      },
      leverage_ratio: {
        name: 'Leverage Ratio',
        unit: '%',
        description: 'Capital to total assets ratio',
        benchmark: { excellent: 8, good: 6, fair: 5, poor: 3 }
      },
      risk_weighted_assets: {
        name: 'Risk Weighted Assets',
        unit: '$ Millions',
        description: 'Total assets weighted by credit risk',
        benchmark: { excellent: 0, good: 0, fair: 0, poor: 0 }
      }
    },
    asset_quality: {
      npl_ratio: {
        name: 'NPL Ratio',
        unit: '%',
        description: 'Non-performing loans as percentage of total loans',
        benchmark: { excellent: 0.5, good: 1.0, fair: 2.0, poor: 3.0 }
      },
      loan_loss_provisions: {
        name: 'Loan Loss Provisions',
        unit: '%',
        description: 'Provisions for credit losses',
        benchmark: { excellent: 0.3, good: 0.5, fair: 1.0, poor: 1.5 }
      },
      coverage_ratio: {
        name: 'Coverage Ratio',
        unit: '%',
        description: 'Loan loss reserves to NPLs ratio',
        benchmark: { excellent: 120, good: 100, fair: 80, poor: 60 }
      },
      asset_classification: {
        name: 'Asset Classification',
        unit: '%',
        description: 'Classified assets percentage',
        benchmark: { excellent: 1, good: 2, fair: 4, poor: 6 }
      }
    },
    profitability: {
      return_on_assets: {
        name: 'Return on Assets',
        unit: '%',
        description: 'Net income as percentage of total assets',
        benchmark: { excellent: 1.5, good: 1.2, fair: 0.8, poor: 0.4 }
      },
      return_on_equity: {
        name: 'Return on Equity',
        unit: '%',
        description: 'Net income as percentage of shareholder equity',
        benchmark: { excellent: 15, good: 12, fair: 8, poor: 4 }
      },
      net_interest_margin: {
        name: 'Net Interest Margin',
        unit: '%',
        description: 'Interest income minus interest expense as percentage of earning assets',
        benchmark: { excellent: 4.0, good: 3.5, fair: 2.5, poor: 1.5 }
      },
      cost_to_income_ratio: {
        name: 'Cost-to-Income Ratio',
        unit: '%',
        description: 'Operating costs as percentage of operating income',
        benchmark: { excellent: 50, good: 60, fair: 70, poor: 80 }
      },
      earnings_per_share: {
        name: 'Earnings Per Share',
        unit: '$',
        description: 'Net income divided by shares outstanding',
        benchmark: { excellent: 10, good: 8, fair: 5, poor: 2 }
      }
    },
    liquidity: {
      liquidity_coverage_ratio: {
        name: 'Liquidity Coverage Ratio',
        unit: '%',
        description: 'High-quality liquid assets to net cash outflows',
        benchmark: { excellent: 130, good: 115, fair: 105, poor: 100 }
      },
      net_stable_funding_ratio: {
        name: 'Net Stable Funding Ratio',
        unit: '%',
        description: 'Available stable funding to required stable funding',
        benchmark: { excellent: 115, good: 110, fair: 105, poor: 100 }
      },
      loan_to_deposit_ratio: {
        name: 'Loan-to-Deposit Ratio',
        unit: '%',
        description: 'Total loans divided by total deposits',
        benchmark: { excellent: 70, good: 80, fair: 90, poor: 100 }
      },
      cash_ratio: {
        name: 'Cash Ratio',
        unit: '%',
        description: 'Cash and equivalents to current liabilities',
        benchmark: { excellent: 15, good: 12, fair: 8, poor: 5 }
      }
    }
  };
}
