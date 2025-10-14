import os
import json
from openai import OpenAI

# the newest OpenAI model is "gpt-5" which was released August 7, 2025.
# do not change this unless explicitly requested by the user
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

def generate_metric_commentary(metric_data, metric_name, institution_name, metric_info):
    """
    Generate AI-powered commentary for a specific metric trend.
    
    Args:
        metric_data: Series or list of metric values over time
        metric_name: Name of the metric
        institution_name: Name of the financial institution
        metric_info: Dictionary containing metric information and benchmarks
    """
    
    if not OPENAI_API_KEY:
        return generate_fallback_commentary(metric_data, metric_name, institution_name, metric_info)
    
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        # Calculate trend statistics
        values = list(metric_data)
        if len(values) < 2:
            return "Insufficient historical data for trend analysis."
        
        current_value = values[-1]
        previous_value = values[-2]
        change = current_value - previous_value
        change_percent = (change / previous_value * 100) if previous_value != 0 else 0
        
        # Prepare context for AI
        trend_context = {
            "institution": institution_name,
            "metric": metric_name,
            "current_value": round(current_value, 2),
            "previous_value": round(previous_value, 2),
            "change": round(change, 2),
            "change_percent": round(change_percent, 2),
            "historical_values": [round(v, 2) for v in values],
            "metric_description": metric_info.get('description', ''),
            "benchmarks": metric_info.get('benchmark', {}),
            "unit": metric_info.get('unit', '')
        }
        
        prompt = f"""
        Analyze the financial metric trend for {institution_name} and provide professional commentary.
        
        Metric Details:
        - Metric: {metric_name} ({metric_info.get('unit', '')})
        - Description: {metric_info.get('description', '')}
        - Current Value: {current_value:.2f}
        - Previous Year Value: {previous_value:.2f}
        - Year-over-Year Change: {change:.2f} ({change_percent:.1f}%)
        - 5-Year Historical Values: {values}
        
        Benchmarks (Good/Fair/Poor thresholds):
        {json.dumps(metric_info.get('benchmark', {}), indent=2)}
        
        Please provide a concise 2-3 sentence professional analysis that:
        1. Describes the trend direction and magnitude
        2. Compares current performance against industry benchmarks
        3. Highlights any risk areas or positive developments
        4. Uses appropriate financial terminology
        
        Format the response as plain text, suitable for a financial dashboard.
        """
        
        response = client.chat.completions.create(
            model="gpt-5",
            messages=[
                {
                    "role": "system",
                    "content": "You are a senior financial analyst specializing in bank credit analysis. Provide clear, professional commentary on financial metrics."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            max_completion_tokens=200
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        return generate_fallback_commentary(metric_data, metric_name, institution_name, metric_info)

def generate_section_commentary(section_data, section_name, institution_name):
    """
    Generate comprehensive commentary for an entire section (e.g., Capitalization, Asset Quality).
    
    Args:
        section_data: Dictionary of metrics for the section
        section_name: Name of the section
        institution_name: Name of the financial institution
    """
    
    if not OPENAI_API_KEY:
        return generate_fallback_section_commentary(section_data, section_name, institution_name)
    
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        # Prepare metrics summary
        metrics_summary = {}
        for metric, values in section_data.items():
            if len(values) >= 2:
                current = values.iloc[-1]
                previous = values.iloc[-2]
                change_pct = ((current - previous) / previous * 100) if previous != 0 else 0
                metrics_summary[metric] = {
                    "current": round(current, 2),
                    "change_percent": round(change_pct, 2)
                }
        
        prompt = f"""
        Provide a comprehensive analysis of the {section_name} performance for {institution_name}.
        
        Current Metrics and Year-over-Year Changes:
        {json.dumps(metrics_summary, indent=2)}
        
        Please provide a professional 3-4 sentence analysis that:
        1. Summarizes the overall {section_name.lower()} position
        2. Identifies key strengths and weaknesses
        3. Highlights the most significant changes
        4. Provides forward-looking assessment of risks/opportunities
        
        Use appropriate banking terminology and focus on credit analysis perspective.
        Format as plain text suitable for executive summary.
        """
        
        response = client.chat.completions.create(
            model="gpt-5",
            messages=[
                {
                    "role": "system",
                    "content": "You are a senior credit analyst providing executive-level commentary on bank financial performance."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_completion_tokens=300
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        return generate_fallback_section_commentary(section_data, section_name, institution_name)

def generate_overall_commentary(bank_data, institution_name, overall_score):
    """
    Generate comprehensive commentary for the overall credit assessment.
    
    Args:
        bank_data: Complete bank data dictionary
        institution_name: Name of the financial institution
        overall_score: Overall credit score
    """
    
    if not OPENAI_API_KEY:
        return generate_fallback_overall_commentary(bank_data, institution_name, overall_score)
    
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        # Get latest year data
        latest_data = bank_data['historical_data'].iloc[-1]
        
        # Key metrics summary
        key_metrics = {
            "Capital Adequacy": latest_data['capital_adequacy_ratio'],
            "NPL Ratio": latest_data['npl_ratio'], 
            "Return on Assets": latest_data['return_on_assets'],
            "Liquidity Coverage": latest_data['liquidity_coverage_ratio'],
            "Overall Score": overall_score
        }
        
        prompt = f"""
        Provide an executive summary credit analysis for {institution_name}.
        
        Overall Credit Score: {overall_score:.1f}/10.0
        
        Key Performance Indicators:
        {json.dumps(key_metrics, indent=2)}
        
        Institution Details:
        - Type: {bank_data.get('institution_type', 'Bank')}
        - Total Assets: ${bank_data.get('assets', 0):,.0f} million
        - Employees: {bank_data.get('employees', 0):,}
        
        Please provide a comprehensive 4-5 sentence executive summary that:
        1. Opens with overall credit assessment and rating rationale
        2. Highlights key financial strengths
        3. Identifies primary areas of concern or risk
        4. Provides outlook and recommendation for credit decision
        5. References specific metrics to support conclusions
        
        Write in executive summary style appropriate for senior management review.
        """
        
        response = client.chat.completions.create(
            model="gpt-5",
            messages=[
                {
                    "role": "system",
                    "content": "You are a senior credit officer preparing executive summaries for credit committee review."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_completion_tokens=400
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        return generate_fallback_overall_commentary(bank_data, institution_name, overall_score)

def generate_fallback_commentary(metric_data, metric_name, institution_name, metric_info):
    """Generate basic commentary when AI is not available."""
    values = list(metric_data)
    if len(values) < 2:
        return "Insufficient historical data for analysis."
    
    current = values[-1]
    previous = values[-2]
    change = current - previous
    change_pct = (change / previous * 100) if previous != 0 else 0
    
    trend = "increased" if change > 0 else "decreased" if change < 0 else "remained stable"
    
    # Basic benchmark comparison
    benchmark = metric_info.get('benchmark', {})
    performance = "within acceptable ranges"
    
    if benchmark.get('good') and benchmark.get('fair'):
        good_threshold = benchmark['good']
        fair_threshold = benchmark['fair']
        
        if good_threshold > fair_threshold:  # Higher is better
            if current >= good_threshold:
                performance = "performing well above industry benchmarks"
            elif current >= fair_threshold:
                performance = "meeting industry standards"
            else:
                performance = "below industry benchmarks and requires attention"
        else:  # Lower is better
            if current <= good_threshold:
                performance = "performing well above industry benchmarks"
            elif current <= fair_threshold:
                performance = "meeting industry standards"
            else:
                performance = "above industry benchmarks and requires attention"
    
    return f"{institution_name}'s {metric_name} {trend} by {abs(change_pct):.1f}% year-over-year to {current:.2f}{metric_info.get('unit', '')}. The current level is {performance}."

def generate_fallback_section_commentary(section_data, section_name, institution_name):
    """Generate basic section commentary when AI is not available."""
    improving_metrics = 0
    declining_metrics = 0
    
    for metric, values in section_data.items():
        if len(values) >= 2:
            if values.iloc[-1] > values.iloc[-2]:
                improving_metrics += 1
            elif values.iloc[-1] < values.iloc[-2]:
                declining_metrics += 1
    
    if improving_metrics > declining_metrics:
        trend = "showing overall improvement"
    elif declining_metrics > improving_metrics:
        trend = "showing some areas of concern"
    else:
        trend = "remaining relatively stable"
    
    return f"{institution_name}'s {section_name.lower()} metrics are {trend} based on year-over-year performance across key indicators. Management should continue monitoring these trends closely."

def generate_fallback_overall_commentary(bank_data, institution_name, overall_score):
    """Generate basic overall commentary when AI is not available."""
    
    if overall_score >= 8.0:
        assessment = "demonstrates strong financial health"
        recommendation = "presents low credit risk"
    elif overall_score >= 6.5:
        assessment = "shows solid financial performance" 
        recommendation = "represents moderate credit risk"
    elif overall_score >= 5.0:
        assessment = "exhibits mixed financial indicators"
        recommendation = "requires careful monitoring"
    else:
        assessment = "shows areas of financial concern"
        recommendation = "presents elevated credit risk"
    
    return f"{institution_name} {assessment} with an overall credit score of {overall_score:.1f}/10.0. The institution {recommendation} based on current capitalization, asset quality, profitability, and liquidity metrics."
