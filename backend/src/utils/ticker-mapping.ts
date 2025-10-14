// Ticker symbol mapping for financial institutions
export const TICKER_MAPPING: Record<string, string> = {
  "JPMorgan Chase & Co.": "JPM",
  "Bank of America Corporation": "BAC",
  "Wells Fargo & Company": "WFC",
  "Citigroup Inc.": "C",
  "Goldman Sachs Group Inc.": "GS",
  "Morgan Stanley": "MS",
  "U.S. Bancorp": "USB",
  "Truist Financial Corporation": "TFC",
  "PNC Financial Services Group": "PNC",
  "Charles Schwab Corporation": "SCHW"
};

// CIK (Central Index Key) mapping for SEC EDGAR API
export const CIK_MAPPING: Record<string, string> = {
  "JPMorgan Chase & Co.": "0000019617",
  "Bank of America Corporation": "0000070858",
  "Wells Fargo & Company": "0000072971",
  "Citigroup Inc.": "0000831001",
  "Goldman Sachs Group Inc.": "0000886982",
  "Morgan Stanley": "0000895421",
  "U.S. Bancorp": "0000036104",
  "Truist Financial Corporation": "0000092230",
  "PNC Financial Services Group": "0000713676",
  "Charles Schwab Corporation": "0000316709"
};

export function getTickerByName(institutionName: string): string | undefined {
  return TICKER_MAPPING[institutionName];
}

export function getCIKByName(institutionName: string): string | undefined {
  return CIK_MAPPING[institutionName];
}
