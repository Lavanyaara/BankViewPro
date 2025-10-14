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
  "Charles Schwab Corporation": "SCHW",
  "Fidelity Investments": "FNF",
  "Interactive Brokers": "IBKR",
  "LPL Financial": "LPLA",
  "Raymond James Financial": "RJF",
  "E*TRADE Financial": "ETFC"
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
  "Charles Schwab Corporation": "0000316709",
  "Fidelity Investments": "0000801109",
  "Interactive Brokers": "0001436320",
  "LPL Financial": "0001414932",
  "Raymond James Financial": "0000720005",
  "E*TRADE Financial": "0001015780"
};

// FINRA CRD (Central Registration Depository) numbers for broker-dealers
export const FINRA_CRD_MAPPING: Record<string, string> = {
  "Charles Schwab Corporation": "5393",
  "Fidelity Investments": "7784",
  "Interactive Brokers": "36418",
  "LPL Financial": "6413",
  "Raymond James Financial": "705",
  "E*TRADE Financial": "29106"
};

// RSSD IDs for FFIEC Call Reports (banks)
export const RSSD_MAPPING: Record<string, string> = {
  "JPMorgan Chase & Co.": "852218",
  "Bank of America Corporation": "1073757",
  "Wells Fargo & Company": "451965",
  "Citigroup Inc.": "1951350",
  "Goldman Sachs Group Inc.": "2380443",
  "Morgan Stanley": "1456501",
  "U.S. Bancorp": "504713",
  "Truist Financial Corporation": "2277860",
  "PNC Financial Services Group": "817824"
};

export function getTickerByName(institutionName: string): string | undefined {
  return TICKER_MAPPING[institutionName];
}

export function getCIKByName(institutionName: string): string | undefined {
  return CIK_MAPPING[institutionName];
}

export function getCRDByName(institutionName: string): string | undefined {
  return FINRA_CRD_MAPPING[institutionName];
}

export function getRSSDByName(institutionName: string): string | undefined {
  return RSSD_MAPPING[institutionName];
}
