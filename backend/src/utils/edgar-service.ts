import axios from 'axios';
import { getCIKByName } from './ticker-mapping';

interface SECFiling {
  accessionNumber: string;
  filingDate: string;
  reportDate: string;
  acceptanceDateTime: string;
  form: string;
  fileNumber: string;
  items: string;
  size: number;
  primaryDocument: string;
  primaryDocDescription: string;
}

interface SECSubmissionsResponse {
  cik: string;
  entityType: string;
  sic: string;
  sicDescription: string;
  name: string;
  filings: {
    recent: {
      accessionNumber: string[];
      filingDate: string[];
      reportDate: string[];
      acceptanceDateTime: string[];
      form: string[];
      fileNumber: string[];
      items: string[];
      size: number[];
      primaryDocument: string[];
      primaryDocDescription: string[];
    };
  };
}

export class EdgarService {
  private static readonly BASE_URL = 'https://data.sec.gov';
  private static readonly EDGAR_BASE = 'https://www.sec.gov/Archives/edgar/data';
  private static readonly USER_AGENT = 'CreditDashboard/1.0 (replit.app)';

  /**
   * Fetch company submissions from SEC EDGAR
   */
  static async getCompanySubmissions(cik: string): Promise<SECSubmissionsResponse> {
    const url = `${this.BASE_URL}/submissions/CIK${cik}.json`;
    
    const response = await axios.get(url, {
      headers: {
        'User-Agent': this.USER_AGENT,
        'Accept': 'application/json'
      }
    });

    return response.data;
  }

  /**
   * Get the most recent 10-K and 10-Q filings for an institution
   */
  static async getRecentFilings(institutionName: string): Promise<{
    tenK?: SECFiling;
    tenQ?: SECFiling;
  }> {
    const cik = getCIKByName(institutionName);
    
    if (!cik) {
      throw new Error(`No CIK found for institution: ${institutionName}`);
    }

    const submissions = await this.getCompanySubmissions(cik);
    const filings = submissions.filings.recent;

    // Find most recent 10-K
    const tenKIndex = filings.form.findIndex(form => form === '10-K');
    const tenK = tenKIndex !== -1 ? {
      accessionNumber: filings.accessionNumber[tenKIndex],
      filingDate: filings.filingDate[tenKIndex],
      reportDate: filings.reportDate[tenKIndex],
      acceptanceDateTime: filings.acceptanceDateTime[tenKIndex],
      form: filings.form[tenKIndex],
      fileNumber: filings.fileNumber[tenKIndex],
      items: filings.items[tenKIndex],
      size: filings.size[tenKIndex],
      primaryDocument: filings.primaryDocument[tenKIndex],
      primaryDocDescription: filings.primaryDocDescription[tenKIndex]
    } : undefined;

    // Find most recent 10-Q
    const tenQIndex = filings.form.findIndex(form => form === '10-Q');
    const tenQ = tenQIndex !== -1 ? {
      accessionNumber: filings.accessionNumber[tenQIndex],
      filingDate: filings.filingDate[tenQIndex],
      reportDate: filings.reportDate[tenQIndex],
      acceptanceDateTime: filings.acceptanceDateTime[tenQIndex],
      form: filings.form[tenQIndex],
      fileNumber: filings.fileNumber[tenQIndex],
      items: filings.items[tenQIndex],
      size: filings.size[tenQIndex],
      primaryDocument: filings.primaryDocument[tenQIndex],
      primaryDocDescription: filings.primaryDocDescription[tenQIndex]
    } : undefined;

    return { tenK, tenQ };
  }

  /**
   * Download filing content
   */
  static async getFilingContent(cik: string, accessionNumber: string, primaryDocument: string): Promise<string> {
    // Remove dashes from accession number for URL
    const accessionNoSlash = accessionNumber.replace(/-/g, '');
    const url = `${this.EDGAR_BASE}/${parseInt(cik)}/${accessionNoSlash}/${primaryDocument}`;

    const response = await axios.get(url, {
      headers: {
        'User-Agent': this.USER_AGENT,
        'Accept': 'text/html,application/xhtml+xml'
      },
      timeout: 30000 // 30 second timeout
    });

    return response.data;
  }

  /**
   * Extract text from HTML filing
   */
  static extractTextFromHTML(htmlContent: string): string {
    // Remove script and style tags
    let text = htmlContent.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '');
    text = text.replace(/<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>/gi, '');
    
    // Remove HTML tags
    text = text.replace(/<[^>]+>/g, ' ');
    
    // Decode HTML entities
    text = text.replace(/&nbsp;/g, ' ');
    text = text.replace(/&amp;/g, '&');
    text = text.replace(/&lt;/g, '<');
    text = text.replace(/&gt;/g, '>');
    text = text.replace(/&quot;/g, '"');
    
    // Clean up whitespace
    text = text.replace(/\s+/g, ' ');
    text = text.trim();
    
    return text;
  }

  /**
   * Get filing documents for analysis
   */
  static async getFilingDocumentsForAnalysis(institutionName: string): Promise<{
    tenKText?: string;
    tenQText?: string;
    filingInfo: any;
  }> {
    const cik = getCIKByName(institutionName);
    
    if (!cik) {
      throw new Error(`No CIK found for institution: ${institutionName}`);
    }

    const filings = await this.getRecentFilings(institutionName);
    
    let tenKText: string | undefined;
    let tenQText: string | undefined;

    // Fetch 10-K content
    if (filings.tenK) {
      const htmlContent = await this.getFilingContent(
        cik,
        filings.tenK.accessionNumber,
        filings.tenK.primaryDocument
      );
      tenKText = this.extractTextFromHTML(htmlContent);
    }

    // Fetch 10-Q content
    if (filings.tenQ) {
      const htmlContent = await this.getFilingContent(
        cik,
        filings.tenQ.accessionNumber,
        filings.tenQ.primaryDocument
      );
      tenQText = this.extractTextFromHTML(htmlContent);
    }

    return {
      tenKText,
      tenQText,
      filingInfo: {
        tenK: filings.tenK,
        tenQ: filings.tenQ
      }
    };
  }
}
