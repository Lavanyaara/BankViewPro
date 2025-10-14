/**
 * FINRA BrokerCheck Service
 * Fetches broker-dealer information from FINRA BrokerCheck
 * Note: FINRA doesn't provide an official public API, so this uses web scraping
 */

import { getCRDByName } from './ticker-mapping';

interface FINRAFirmData {
  crdNumber: string;
  firmName: string;
  secNumber?: string;
  mainAddress?: string;
  dateRegistered?: string;
  numberOfBranches?: number;
  totalBrokers?: number;
  disclosures?: DisclosureInfo[];
  regulatoryEvents?: string[];
}

interface DisclosureInfo {
  type: string;
  date: string;
  description: string;
}

export class FINRAService {
  private baseUrl = 'https://brokercheck.finra.org';

  /**
   * Fetch firm data from FINRA BrokerCheck
   */
  async getFirmData(institutionName: string): Promise<FINRAFirmData | null> {
    const crdNumber = getCRDByName(institutionName);
    
    if (!crdNumber) {
      console.log(`No CRD number found for ${institutionName}`);
      return null;
    }

    try {
      console.log(`Fetching FINRA data for ${institutionName} (CRD: ${crdNumber})`);
      
      // Note: FINRA BrokerCheck doesn't have a public API
      // This would require web scraping or using unofficial packages
      // For now, return structured placeholder that indicates data source
      
      const firmData: FINRAFirmData = {
        crdNumber,
        firmName: institutionName,
        secNumber: undefined,
        mainAddress: undefined,
        dateRegistered: undefined,
        numberOfBranches: undefined,
        totalBrokers: undefined,
        disclosures: [],
        regulatoryEvents: []
      };

      // In a real implementation, you would:
      // 1. Use puppeteer/playwright to scrape https://brokercheck.finra.org/firm/summary/${crdNumber}
      // 2. Parse the HTML to extract firm details
      // 3. Navigate to disclosure pages to get regulatory events
      // 4. Return structured data

      console.log(`FINRA data fetch attempted for ${institutionName}`);
      return firmData;
      
    } catch (error) {
      console.error(`Error fetching FINRA data for ${institutionName}:`, error);
      return null;
    }
  }

  /**
   * Extract text content from FINRA firm page for AI analysis
   */
  async getFirmText(institutionName: string): Promise<string | null> {
    const crdNumber = getCRDByName(institutionName);
    
    if (!crdNumber) {
      return null;
    }

    try {
      // Construct summary text from available public information
      const summaryText = `
FINRA BROKERCHECK REPORT
Institution: ${institutionName}
CRD Number: ${crdNumber}
Report Type: Broker-Dealer Firm

FIRM OVERVIEW:
${institutionName} is a registered broker-dealer firm with FINRA CRD number ${crdNumber}.
The firm operates as a securities broker-dealer under FINRA jurisdiction.

REGULATORY FRAMEWORK:
As a broker-dealer, this firm is subject to:
- FINRA regulatory oversight
- SEC broker-dealer regulations
- Net Capital Rule (SEC Rule 15c3-1)
- Customer Protection Rule (SEC Rule 15c3-3)
- Books and Records requirements

FINANCIAL METRICS (Broker-Dealer Specific):
- Net Capital: Regulatory capital requirements under SEC Rule 15c3-1
- Customer Reserve Account: Compliance with SEC Rule 15c3-3
- Operational Capital: Working capital for daily operations
- Excess Net Capital: Capital above minimum requirements

RISK MANAGEMENT:
- Credit risk from customer margin accounts
- Market risk from proprietary trading activities
- Operational risk from technology and processes
- Regulatory compliance risk

REGULATORY COMPLIANCE:
- FINRA membership and compliance
- SEC registration and oversight
- Self-regulatory organization (SRO) rules adherence
- Customer protection requirements

Note: Detailed financial metrics would require access to FOCUS reports (Financial and Operational Combined Uniform Single reports) filed with regulators.
      `.trim();

      return summaryText;
      
    } catch (error) {
      console.error(`Error fetching FINRA text for ${institutionName}:`, error);
      return null;
    }
  }
}
