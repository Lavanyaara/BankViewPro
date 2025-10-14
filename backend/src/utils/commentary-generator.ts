import OpenAI from 'openai';
import { Institution, CategoryScores } from '../../../shared/interfaces';

const openai = process.env.OPENAI_API_KEY
  ? new OpenAI({ apiKey: process.env.OPENAI_API_KEY })
  : null;

export async function generateCommentary(
  institution: Institution,
  scores: CategoryScores,
  category: string
): Promise<string> {
  if (!openai) {
    return getDefaultCommentary(institution, scores, category);
  }

  try {
    const latestData = institution.historical_data[institution.historical_data.length - 1];
    const previousData = institution.historical_data[institution.historical_data.length - 2];

    const prompt = buildPrompt(institution, latestData, previousData, scores, category);

    const completion = await openai.chat.completions.create({
      model: 'gpt-4o',
      messages: [
        {
          role: 'system',
          content: 'You are a financial analyst providing concise, professional commentary on bank credit metrics. Keep responses to 2-3 sentences focused on key insights.'
        },
        {
          role: 'user',
          content: prompt
        }
      ],
      temperature: 0.7,
      max_tokens: 150
    });

    return completion.choices[0]?.message?.content || getDefaultCommentary(institution, scores, category);
  } catch (error) {
    console.error('Error generating commentary:', error);
    return getDefaultCommentary(institution, scores, category);
  }
}

function buildPrompt(
  institution: Institution,
  latestData: any,
  previousData: any,
  scores: CategoryScores,
  category: string
): string {
  const institutionName = institution.institution_name;

  switch (category) {
    case 'capitalization':
      return `Analyze ${institutionName}'s capital position. CAR: ${latestData.capital_adequacy_ratio.toFixed(1)}% (previous: ${previousData.capital_adequacy_ratio.toFixed(1)}%), Tier 1: ${latestData.tier1_ratio.toFixed(1)}%. Score: ${scores.capitalization.toFixed(1)}/10. Provide brief insight.`;

    case 'asset_quality':
      return `Analyze ${institutionName}'s asset quality. NPL ratio: ${latestData.npl_ratio.toFixed(2)}% (previous: ${previousData.npl_ratio.toFixed(2)}%), Coverage: ${latestData.coverage_ratio.toFixed(0)}%. Score: ${scores.asset_quality.toFixed(1)}/10. Provide brief insight.`;

    case 'profitability':
      return `Analyze ${institutionName}'s profitability. ROA: ${latestData.return_on_assets.toFixed(2)}%, ROE: ${latestData.return_on_equity.toFixed(1)}%, NIM: ${latestData.net_interest_margin.toFixed(2)}%. Score: ${scores.profitability.toFixed(1)}/10. Provide brief insight.`;

    case 'liquidity':
      return `Analyze ${institutionName}'s liquidity position. LCR: ${latestData.liquidity_coverage_ratio.toFixed(0)}%, NSFR: ${latestData.net_stable_funding_ratio.toFixed(0)}%. Score: ${scores.liquidity.toFixed(1)}/10. Provide brief insight.`;

    case 'overview':
      return `Provide executive summary for ${institutionName}. Overall credit score: ${scores.overall.toFixed(1)}/10. Key strengths and concerns across capitalization (${scores.capitalization.toFixed(1)}), asset quality (${scores.asset_quality.toFixed(1)}), profitability (${scores.profitability.toFixed(1)}), and liquidity (${scores.liquidity.toFixed(1)}).`;

    default:
      return `Analyze ${institutionName}'s overall financial health with score ${scores.overall.toFixed(1)}/10.`;
  }
}

function getDefaultCommentary(
  institution: Institution,
  scores: CategoryScores,
  category: string
): string {
  const institutionName = institution.institution_name;

  switch (category) {
    case 'capitalization':
      if (scores.capitalization >= 7) {
        return `${institutionName} maintains strong capital levels with ratios well above regulatory minimums, providing robust buffers against potential losses.`;
      }
      return `${institutionName}'s capital position shows adequate levels, though there is room for improvement in building additional buffers.`;

    case 'asset_quality':
      if (scores.asset_quality >= 7) {
        return `${institutionName} demonstrates excellent asset quality with low non-performing loans and strong coverage ratios, indicating effective risk management.`;
      }
      return `${institutionName}'s asset quality metrics are within acceptable ranges, though monitoring of credit risk trends is recommended.`;

    case 'profitability':
      if (scores.profitability >= 7) {
        return `${institutionName} shows strong profitability metrics with healthy returns on assets and equity, reflecting efficient operations and solid earnings capacity.`;
      }
      return `${institutionName}'s profitability indicators are moderate, suggesting opportunities for operational efficiency improvements.`;

    case 'liquidity':
      if (scores.liquidity >= 7) {
        return `${institutionName} maintains robust liquidity buffers well above regulatory requirements, ensuring strong ability to meet short-term obligations.`;
      }
      return `${institutionName}'s liquidity position meets regulatory standards, though additional buffers would enhance financial flexibility.`;

    case 'overview':
      if (scores.overall >= 7) {
        return `${institutionName} demonstrates strong overall credit quality across key metrics, with well-capitalized positions and healthy profitability supporting a stable credit profile.`;
      }
      return `${institutionName} maintains adequate credit metrics overall, with opportunities for strengthening certain areas to enhance the overall credit profile.`;

    default:
      return `${institutionName} maintains a solid financial position with balanced performance across key credit metrics.`;
  }
}
