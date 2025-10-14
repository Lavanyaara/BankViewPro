import OpenAI from 'openai';

const ANALYSIS_PROMPT_TEMPLATE = `For each of the five areas below, write 3–4 short, factual, and objective lines summarizing the relevant information. Every line must be based solely on the provided documents — do not include any external data, interpretation, or assumptions.
After each line, cite the exact source in parentheses — mention the document name and location (e.g., 10-K p. 88, 10-Q Table 7, Call Report – Schedule RC-R Part I).
If there is no explicit information about a point, clearly write: "No explicit information available in the documents regarding this point."
Keep your writing concise and analytical, using quantitative figures where available (e.g., capital ratios, profitability metrics, loss provisions, etc.).

1. Business Environment

Summarize the key macroeconomic and market factors affecting the company's business during the reporting period (e.g., interest rate trends, inflation, demand patterns, or credit conditions).
Include any major external events, policy or regulatory changes, or industry-level developments that directly influenced the company's performance.
Quantify the effects where possible using figures explicitly disclosed in the documents (e.g., NIM, cost of funds, credit losses, GDP impact).
Focus on factual cause-and-effect relationships mentioned in the filings.

2. Company's Market Position

Describe the company's position in its sector, including details on market share, customer base, geographic reach, and product or service diversification.
Identify major business segments and summarize their contribution to revenue and profitability.
Include relevant performance metrics such as ROA, ROE, or net income trends to contextualize market strength.
Mention competitive dynamics, partnerships, or key customer programs if explicitly stated in the filings.

3. Risk Management

Identify the major categories of risk the company faces (credit, liquidity, market, operational, regulatory, etc.).
Highlight specific risk exposures or incidents disclosed, such as delinquency rates, charge-offs, or capital buffer levels.
Note any stress-test outcomes, concentration risks, or emerging threats discussed in the reports.
Focus on measurable risk indicators and actual exposures rather than policy descriptions or generalized statements.

4. Management Quality

Summarize the company's governance and oversight structure, including board composition, independent directors, and committee arrangements (audit, risk, compensation, etc.).
Include any disclosed events such as mergers, acquisitions, CEO transitions, restructuring, or changes in executive management.
Reference formal governance disclosures or charters mentioned in the filings.
Do not include any subjective judgments or external assessments of management capability.

5. Regulatory Compliance, Legal Proceedings, and Liquidity Risk

Summarize the company's regulatory framework, supervision structure, and capital adequacy standards (e.g., CET1, Tier 1, leverage ratios).
Include any information on liquidity management, such as reserves, funding sources, or liquidity coverage ratios, citing relevant tables or schedules.
Explicitly identify any ongoing legal proceedings, investigations, or litigations disclosed in the filings, and note the nature of the exposure (financial or operational).
Mention whether the filings indicate that such exposures are covered, immaterial, or materially significant to the company's financial position.
Cite all legal and compliance references (e.g., 10-K Item 3 – Legal Proceedings, 10-Q Part II Item 1A – Risk Factors, Call Report – Schedule RC-O).

Formatting instructions:

Use numbered sections (1–5).
Keep each section to 3–4 concise bullet points.
Place document references after each line.
Do not infer or assume; include only what is explicitly written in the provided documents.
Maintain a neutral, analytical tone focused on factual disclosure.`;

interface AnalysisResult {
  businessEnvironment: string;
  marketPosition: string;
  riskManagement: string;
  managementQuality: string;
  regulatoryCompliance: string;
  fullAnalysis: string;
}

export interface ExtractedMetrics {
  // Profitability
  roe?: number; // Return on Equity
  roa?: number; // Return on Assets
  nim?: number; // Net Interest Margin
  
  // Capital
  cet1Ratio?: number; // Common Equity Tier 1
  tier1Ratio?: number; // Tier 1 Capital Ratio
  totalCapitalRatio?: number;
  leverageRatio?: number;
  
  // Liquidity
  lcr?: number; // Liquidity Coverage Ratio
  nsfr?: number; // Net Stable Funding Ratio
  
  // Asset Quality
  nplRatio?: number; // Non-Performing Loan Ratio
  chargeOffRate?: number;
  loanLossProvisions?: number;
  
  // Other
  netIncome?: number;
  totalAssets?: number;
  totalEquity?: number;
}

export class SECAnalysisService {
  private openai: OpenAI;

  constructor(apiKey?: string) {
    this.openai = new OpenAI({
      apiKey: apiKey || process.env.OPENAI_API_KEY
    });
  }

  /**
   * Analyze SEC filings using AI
   */
  async analyzeFilings(
    institutionName: string,
    tenKText?: string,
    tenQText?: string
  ): Promise<AnalysisResult> {
    if (!tenKText && !tenQText) {
      throw new Error('At least one filing document (10-K or 10-Q) is required for analysis');
    }

    // Prepare the documents
    let documentsText = '';
    if (tenKText) {
      // Truncate 10-K to stay within token limits (keep first 50k chars)
      const truncatedTenK = tenKText.substring(0, 50000);
      documentsText += `\n\n=== 10-K FILING ===\n${truncatedTenK}\n`;
    }
    if (tenQText) {
      // Truncate 10-Q to stay within token limits (keep first 30k chars)
      const truncatedTenQ = tenQText.substring(0, 30000);
      documentsText += `\n\n=== 10-Q FILING ===\n${truncatedTenQ}\n`;
    }

    const userPrompt = `Institution: ${institutionName}\n\nDocuments to analyze:${documentsText}\n\nPlease analyze these documents according to the instructions above.`;

    try {
      const completion = await this.openai.chat.completions.create({
        model: 'gpt-4o-mini',
        messages: [
          { role: 'system', content: ANALYSIS_PROMPT_TEMPLATE + '\n\nIMPORTANT: After your analysis, add a METRICS SUMMARY section with exact labeled values in this format:\nMETRICS SUMMARY:\nROE: [value]%\nROA: [value]%\nNIM: [value]%\nCET1: [value]%\nTier 1: [value]%\nLeverage Ratio: [value]%\nLCR: [value]%\nNSFR: [value]%\nNPL Ratio: [value]%\nCharge-off Rate: [value]%\n\nOnly include metrics explicitly found in the documents. Use "N/A" if not available.' },
          { role: 'user', content: userPrompt }
        ],
        temperature: 0.3, // Lower temperature for factual analysis
        max_tokens: 4000
      });

      const fullAnalysis = completion.choices[0]?.message?.content || '';

      // Parse sections from the analysis
      const sections = this.parseSections(fullAnalysis);

      return {
        businessEnvironment: sections['1'] || '',
        marketPosition: sections['2'] || '',
        riskManagement: sections['3'] || '',
        managementQuality: sections['4'] || '',
        regulatoryCompliance: sections['5'] || '',
        fullAnalysis
      };
    } catch (error) {
      console.error('OpenAI analysis error:', error);
      throw error;
    }
  }

  /**
   * Parse sections from AI analysis
   */
  private parseSections(analysisText: string): Record<string, string> {
    const sections: Record<string, string> = {};
    const sectionRegex = /(\d+)\.\s*([^\n]+)([\s\S]*?)(?=\d+\.\s+[^\n]+|$)/g;
    
    let match;
    while ((match = sectionRegex.exec(analysisText)) !== null) {
      const [, sectionNum, sectionTitle, sectionContent] = match;
      sections[sectionNum] = (sectionTitle + sectionContent).trim();
    }

    return sections;
  }

  /**
   * Extract metrics from analysis text
   */
  extractMetrics(analysisText: string): ExtractedMetrics {
    const metrics: ExtractedMetrics = {};

    // Look for METRICS SUMMARY section first (more reliable)
    const summaryMatch = analysisText.match(/METRICS SUMMARY:([\s\S]*?)(?:\n\n|$)/i);
    if (summaryMatch) {
      const summaryText = summaryMatch[1];
      
      const roeMatch = summaryText.match(/ROE[:\s]+(\d+\.?\d*)/i);
      if (roeMatch && !roeMatch[1].includes('N/A')) metrics.roe = parseFloat(roeMatch[1]);
      
      const roaMatch = summaryText.match(/ROA[:\s]+(\d+\.?\d*)/i);
      if (roaMatch && !roaMatch[1].includes('N/A')) metrics.roa = parseFloat(roaMatch[1]);
      
      const nimMatch = summaryText.match(/NIM[:\s]+(\d+\.?\d*)/i);
      if (nimMatch && !nimMatch[1].includes('N/A')) metrics.nim = parseFloat(nimMatch[1]);
      
      const cet1Match = summaryText.match(/CET1[:\s]+(\d+\.?\d*)/i);
      if (cet1Match && !cet1Match[1].includes('N/A')) metrics.cet1Ratio = parseFloat(cet1Match[1]);
      
      const tier1Match = summaryText.match(/Tier\s*1[:\s]+(\d+\.?\d*)/i);
      if (tier1Match && !tier1Match[1].includes('N/A')) metrics.tier1Ratio = parseFloat(tier1Match[1]);
      
      const leverageMatch = summaryText.match(/Leverage\s*Ratio[:\s]+(\d+\.?\d*)/i);
      if (leverageMatch && !leverageMatch[1].includes('N/A')) metrics.leverageRatio = parseFloat(leverageMatch[1]);
      
      const lcrMatch = summaryText.match(/LCR[:\s]+(\d+\.?\d*)/i);
      if (lcrMatch && !lcrMatch[1].includes('N/A')) metrics.lcr = parseFloat(lcrMatch[1]);
      
      const nsfrMatch = summaryText.match(/NSFR[:\s]+(\d+\.?\d*)/i);
      if (nsfrMatch && !nsfrMatch[1].includes('N/A')) metrics.nsfr = parseFloat(nsfrMatch[1]);
      
      const nplMatch = summaryText.match(/NPL\s*Ratio[:\s]+(\d+\.?\d*)/i);
      if (nplMatch && !nplMatch[1].includes('N/A')) metrics.nplRatio = parseFloat(nplMatch[1]);
      
      const chargeOffMatch = summaryText.match(/Charge-?off\s*Rate[:\s]+(\d+\.?\d*)/i);
      if (chargeOffMatch && !chargeOffMatch[1].includes('N/A')) metrics.chargeOffRate = parseFloat(chargeOffMatch[1]);
    } else {
      // Fallback to finding in main text with more flexible patterns
      const patterns = [
        { key: 'roe', regex: /(?:ROE|return on equity)[:\s]*(?:≈\s*)?(\d+\.?\d*)\s*%/i },
        { key: 'roa', regex: /(?:ROA|return on assets)[:\s]*(?:≈\s*)?(\d+\.?\d*)\s*%/i },
        { key: 'nim', regex: /(?:NIM|net interest margin)[:\s]*(?:≈\s*)?(\d+\.?\d*)\s*%/i },
        { key: 'cet1Ratio', regex: /(?:CET1|common equity tier 1)[:\s]*(?:≈\s*)?(\d+\.?\d*)\s*%/i },
        { key: 'tier1Ratio', regex: /tier\s*1(?:\s+capital)?\s*ratio[:\s]*(?:≈\s*)?(\d+\.?\d*)\s*%/i },
        { key: 'leverageRatio', regex: /leverage\s*ratio[:\s]*(?:≈\s*)?(\d+\.?\d*)\s*%/i },
        { key: 'lcr', regex: /(?:LCR|liquidity coverage ratio)[:\s]*(?:≈\s*)?(\d+\.?\d*)\s*%/i },
        { key: 'nsfr', regex: /(?:NSFR|net stable funding ratio)[:\s]*(?:≈\s*)?(\d+\.?\d*)\s*%/i },
        { key: 'nplRatio', regex: /(?:NPL|non-performing loan)\s*ratio[:\s]*(?:≈\s*)?(\d+\.?\d*)\s*%/i },
        { key: 'chargeOffRate', regex: /charge-?off\s*rate[:\s]*(?:≈\s*)?(\d+\.?\d*)\s*%/i }
      ];

      for (const { key, regex } of patterns) {
        const match = analysisText.match(regex);
        if (match) {
          (metrics as any)[key] = parseFloat(match[1]);
        }
      }
    }

    return metrics;
  }

  /**
   * Generate fallback analysis when OpenAI fails
   */
  generateFallbackAnalysis(institutionName: string): AnalysisResult {
    return {
      businessEnvironment: `SEC filing analysis unavailable for ${institutionName}. Unable to access OpenAI API.`,
      marketPosition: 'Analysis unavailable.',
      riskManagement: 'Analysis unavailable.',
      managementQuality: 'Analysis unavailable.',
      regulatoryCompliance: 'Analysis unavailable.',
      fullAnalysis: `Analysis service unavailable for ${institutionName}. Please check API configuration.`
    };
  }
}
