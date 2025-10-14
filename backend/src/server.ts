import express, { Request, Response } from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import { generateSampleData, getMetricInfo } from './utils/data-generator';
import { calculateOverallScore, getRatingLabel } from './utils/scoring-engine';
import { generateCommentary } from './utils/commentary-generator';
import { EdgarService } from './utils/edgar-service';
import { SECAnalysisService } from './utils/sec-analysis-service';
import { MetricsMapper } from './utils/metrics-mapper';
import { EdgarCache } from './utils/edgar-cache';
import { FINRAService } from './utils/finra-service';
import { FFIECService } from './utils/ffiec-service';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

const bankData = generateSampleData();
const metricInfo = getMetricInfo();
const analysisService = new SECAnalysisService();
const finraService = new FINRAService();
const ffiecService = new FFIECService();

// Helper function to extract category-specific text from EDGAR analysis
function extractCategoryFromAnalysis(analysisText: string, category: string): string | null {
  const categoryMap: Record<string, string> = {
    'overview': '1\\. Business Environment|2\\. Company\'s Market Position',
    'capitalization': '5\\. Regulatory Compliance.*?(?:CET1|Tier 1|capital)',
    'asset_quality': '3\\. Risk Management.*?(?:NPL|charge-off|asset quality)',
    'profitability': '2\\. Company\'s Market Position.*?(?:ROE|ROA|profitability)',
    'liquidity': '5\\. Regulatory Compliance.*?(?:LCR|NSFR|liquidity)'
  };

  const pattern = categoryMap[category];
  if (!pattern) return null;

  const regex = new RegExp(`(${pattern}[\\s\\S]{0,500})`, 'i');
  const match = analysisText.match(regex);
  
  return match ? match[1].trim() : null;
}

app.get('/api/institutions', (req: Request, res: Response) => {
  const institutions = Object.keys(bankData).map(name => ({
    name,
    type: bankData[name].institution_type,
    assets: bankData[name].assets,
    employees: bankData[name].employees,
    branches: bankData[name].branches
  }));
  
  res.json(institutions);
});

app.get('/api/institutions/:name', async (req: Request, res: Response) => {
  const name = decodeURIComponent(req.params.name);
  
  // Check if institution exists in our list
  if (!bankData[name]) {
    return res.status(404).json({ error: 'Institution not found' });
  }
  
  const institutionType = bankData[name].institution_type;
  
  try {
    // Try to use cached data first
    const cached = EdgarCache.get(name);
    if (cached) {
      console.log(`Using cached data for ${name} (${institutionType})`);
      return res.json(cached.data);
    }
    
    let combinedAnalysisText = '';
    let analysisResult;
    
    if (institutionType === 'Bank') {
      // Banks: Fetch SEC filings + FFIEC Call Reports
      console.log(`Fetching Bank data for ${name}...`);
      
      // Get SEC filings
      const { tenKText, tenQText } = await EdgarService.getFilingDocumentsForAnalysis(name);
      
      // Get FFIEC Call Report data
      const callReportText = await ffiecService.getCallReportText(name);
      
      // Combine all available data sources
      if (tenKText) combinedAnalysisText += `\n\n=== SEC 10-K FILING ===\n${tenKText.slice(0, 30000)}`;
      if (tenQText) combinedAnalysisText += `\n\n=== SEC 10-Q FILING ===\n${tenQText.slice(0, 20000)}`;
      if (callReportText) combinedAnalysisText += `\n\n=== FFIEC CALL REPORT ===\n${callReportText}`;
      
      if (combinedAnalysisText) {
        console.log(`Analyzing Bank filings and call reports for ${name}...`);
        analysisResult = await analysisService.analyzeFilings(name, combinedAnalysisText, '');
      }
      
    } else {
      // Broker Dealers: Fetch FINRA data + SEC filings if available
      console.log(`Fetching Broker Dealer data for ${name}...`);
      
      // Get FINRA BrokerCheck data
      const finraText = await finraService.getFirmText(name);
      
      // Get SEC filings (broker-dealers often have 10-K too)
      const { tenKText, tenQText } = await EdgarService.getFilingDocumentsForAnalysis(name);
      
      // Combine all available data sources
      if (finraText) combinedAnalysisText += `\n\n=== FINRA BROKERCHECK DATA ===\n${finraText}`;
      if (tenKText) combinedAnalysisText += `\n\n=== SEC 10-K FILING ===\n${tenKText.slice(0, 30000)}`;
      if (tenQText) combinedAnalysisText += `\n\n=== SEC 10-Q FILING ===\n${tenQText.slice(0, 20000)}`;
      
      if (combinedAnalysisText) {
        console.log(`Analyzing Broker Dealer filings and FINRA data for ${name}...`);
        analysisResult = await analysisService.analyzeFilings(name, combinedAnalysisText, '');
      }
    }
    
    if (!analysisResult || !combinedAnalysisText) {
      console.log(`No regulatory data found for ${name}, using synthetic data`);
      return res.json(bankData[name]);
    }
    
    // Extract metrics from analysis
    const extractedMetrics = analysisService.extractMetrics(analysisResult.fullAnalysis);
    
    // Map to dashboard format
    const institutionData = MetricsMapper.mapToInstitution(name, extractedMetrics, analysisResult.fullAnalysis);
    
    // Cache the result
    EdgarCache.set(name, institutionData, analysisResult.fullAnalysis);
    
    console.log(`Successfully fetched and analyzed regulatory data for ${name} (${institutionType})`);
    res.json(institutionData);
  } catch (error) {
    console.error(`Error fetching regulatory data for ${name}:`, error);
    // Fallback to synthetic data
    console.log(`Falling back to synthetic data for ${name}`);
    res.json(bankData[name]);
  }
});

app.get('/api/institutions/:name/scores', (req: Request, res: Response) => {
  const name = decodeURIComponent(req.params.name);
  
  // Check if institution exists
  if (!bankData[name]) {
    return res.status(404).json({ error: 'Institution not found' });
  }
  
  // Try to use cached EDGAR data first, otherwise fall back to synthetic
  const cached = EdgarCache.get(name);
  const institution = cached ? cached.data : bankData[name];
  
  const scores = calculateOverallScore(institution);
  const rating = getRatingLabel(scores.overall);
  
  res.json({ ...scores, rating });
});

app.post('/api/commentary', async (req: Request, res: Response) => {
  const { institutionName, category } = req.body;
  
  if (!institutionName || !category) {
    return res.status(400).json({ error: 'institutionName and category are required' });
  }
  
  // Check if institution exists
  if (!bankData[institutionName]) {
    return res.status(404).json({ error: 'Institution not found' });
  }
  
  // Try to use cached EDGAR data first, otherwise fall back to synthetic
  const cached = EdgarCache.get(institutionName);
  const institution = cached ? cached.data : bankData[institutionName];
  
  // If we have EDGAR analysis text and it contains relevant category info, use it directly
  if (cached && cached.analysisText) {
    const categoryText = extractCategoryFromAnalysis(cached.analysisText, category);
    if (categoryText) {
      return res.json({ commentary: categoryText });
    }
  }
  
  const scores = calculateOverallScore(institution);
  const commentary = await generateCommentary(institution, scores, category);
  
  res.json({ commentary });
});

app.get('/api/metrics', (req: Request, res: Response) => {
  res.json(metricInfo);
});

app.post('/api/chat', async (req: Request, res: Response) => {
  const { institutionName, message, conversationHistory } = req.body;
  
  if (!institutionName || !message) {
    return res.status(400).json({ error: 'institutionName and message are required' });
  }
  
  // Check if institution exists
  if (!bankData[institutionName]) {
    return res.status(404).json({ error: 'Institution not found' });
  }
  
  // Try to use cached EDGAR data first, otherwise fall back to synthetic
  const cached = EdgarCache.get(institutionName);
  const institution = cached ? cached.data : bankData[institutionName];
  
  const scores = calculateOverallScore(institution);
  const latestData = institution.historical_data[institution.historical_data.length - 1];
  
  try {
    const openai = require('openai');
    const client = new openai.OpenAI({
      apiKey: process.env.OPENAI_API_KEY
    });
    
    const systemPrompt = `You are a financial analyst assistant for a credit review dashboard. You have access to financial data for ${institutionName}.

Current Financial Metrics (Latest Year ${latestData.year}):
- Capital Adequacy Ratio: ${latestData.capital_adequacy_ratio.toFixed(2)}%
- Tier 1 Ratio: ${latestData.tier1_ratio.toFixed(2)}%
- NPL Ratio: ${latestData.npl_ratio.toFixed(2)}%
- Return on Assets: ${latestData.return_on_assets.toFixed(2)}%
- Return on Equity: ${latestData.return_on_equity.toFixed(2)}%
- Liquidity Coverage Ratio: ${latestData.liquidity_coverage_ratio.toFixed(2)}%

Credit Scores (1-10 scale):
- Capitalization: ${scores.capitalization.toFixed(1)}/10
- Asset Quality: ${scores.asset_quality.toFixed(1)}/10
- Profitability: ${scores.profitability.toFixed(1)}/10
- Liquidity: ${scores.liquidity.toFixed(1)}/10
- Overall: ${scores.overall.toFixed(1)}/10

Institution Details:
- Type: ${institution.institution_type}
- Total Assets: $${(institution.assets / 1e9).toFixed(1)}B
- Employees: ${institution.employees.toLocaleString()}

Answer questions about this institution's financial health, metrics, and credit rating. Be concise and professional.`;

    const messages = [
      { role: 'system', content: systemPrompt },
      ...(conversationHistory || []).map((msg: any) => ({
        role: msg.role,
        content: msg.content
      })),
      { role: 'user', content: message }
    ];
    
    const completion = await client.chat.completions.create({
      model: 'gpt-4o-mini',
      messages: messages,
      temperature: 0.7,
      max_tokens: 500
    });
    
    const responseMessage = completion.choices[0]?.message?.content || 'I apologize, but I could not generate a response.';
    
    res.json({ message: responseMessage });
  } catch (error) {
    console.error('OpenAI API error:', error);
    
    const fallbackResponse = `I'm analyzing ${institutionName} with an overall credit score of ${scores.overall.toFixed(1)}/10. The institution shows ${scores.capitalization >= 7 ? 'strong' : scores.capitalization >= 5 ? 'moderate' : 'weak'} capitalization, ${scores.asset_quality >= 7 ? 'excellent' : scores.asset_quality >= 5 ? 'adequate' : 'concerning'} asset quality, and ${scores.liquidity >= 7 ? 'robust' : scores.liquidity >= 5 ? 'sufficient' : 'limited'} liquidity. How can I help you understand these metrics better?`;
    
    res.json({ message: fallbackResponse });
  }
});

app.get('/health', (req: Request, res: Response) => {
  res.json({ status: 'healthy', timestamp: new Date().toISOString() });
});

app.listen(PORT, () => {
  console.log(`Credit Dashboard API server running on port ${PORT}`);
  console.log(`Health check: http://localhost:${PORT}/health`);
});
