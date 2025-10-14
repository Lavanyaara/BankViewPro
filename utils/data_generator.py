import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sample_data():
    """
    Generate sample financial data for major US banks and broker dealers.
    This creates realistic-looking financial metrics for demonstration purposes.
    """
    
    # Define banks and broker dealers
    institutions = [
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
    ]
    
    # Generate years (last 5 years)
    current_year = datetime.now().year
    years = list(range(current_year - 4, current_year + 1))
    
    bank_data = {}
    
    for institution in institutions:
        data = {}
        
        # Generate base values that will trend over time
        np.random.seed(hash(institution) % 2**32)  # Consistent data per institution
        
        # Capitalization Metrics
        base_car = np.random.uniform(12, 18)  # Capital Adequacy Ratio
        base_tier1 = np.random.uniform(10, 15)  # Tier 1 Ratio
        base_leverage = np.random.uniform(8, 12)  # Leverage Ratio
        base_rwa = np.random.uniform(800000, 2000000)  # Risk Weighted Assets (millions)
        
        # Asset Quality Metrics
        base_npl = np.random.uniform(0.5, 2.5)  # NPL Ratio
        base_provisions = np.random.uniform(0.3, 1.2)  # Loan Loss Provisions
        base_coverage = np.random.uniform(60, 120)  # Coverage Ratio
        base_classification = np.random.uniform(2, 8)  # Asset Classification
        
        # Profitability Metrics
        base_roa = np.random.uniform(0.8, 1.5)  # Return on Assets
        base_roe = np.random.uniform(8, 15)  # Return on Equity
        base_nim = np.random.uniform(2.5, 4.0)  # Net Interest Margin
        base_cost_income = np.random.uniform(55, 75)  # Cost to Income Ratio
        base_eps = np.random.uniform(4, 12)  # Earnings Per Share
        
        # Liquidity Metrics
        base_lcr = np.random.uniform(110, 150)  # Liquidity Coverage Ratio
        base_nsfr = np.random.uniform(105, 130)  # Net Stable Funding Ratio
        base_ltd = np.random.uniform(70, 90)  # Loan to Deposit Ratio
        base_cash = np.random.uniform(8, 15)  # Cash Ratio
        
        # Generate yearly data with trends
        yearly_data = []
        
        for i, year in enumerate(years):
            # Add some year-over-year variation and trends
            trend_factor = 1 + (i * 0.02 + np.random.normal(0, 0.05))
            volatility = np.random.normal(1, 0.08)
            
            yearly_record = {
                'year': year,
                # Capitalization
                'capital_adequacy_ratio': max(8, base_car * trend_factor * volatility),
                'tier1_ratio': max(6, base_tier1 * trend_factor * volatility),
                'leverage_ratio': max(3, base_leverage * trend_factor * volatility),
                'risk_weighted_assets': base_rwa * (1 + i * 0.1) * volatility,
                
                # Asset Quality (lower is better for NPL, provisions)
                'npl_ratio': max(0.1, base_npl * (1 - i * 0.05) * volatility),
                'loan_loss_provisions': max(0.1, base_provisions * (1 - i * 0.03) * volatility),
                'coverage_ratio': base_coverage * trend_factor * volatility,
                'asset_classification': max(1, base_classification * (1 - i * 0.1) * volatility),
                
                # Profitability
                'return_on_assets': max(0.1, base_roa * trend_factor * volatility),
                'return_on_equity': max(2, base_roe * trend_factor * volatility),
                'net_interest_margin': max(1, base_nim * trend_factor * volatility),
                'cost_to_income_ratio': max(40, min(90, base_cost_income * (1 - i * 0.02) * volatility)),
                'earnings_per_share': max(1, base_eps * trend_factor * volatility),
                
                # Liquidity
                'liquidity_coverage_ratio': max(100, base_lcr * trend_factor * volatility),
                'net_stable_funding_ratio': max(100, base_nsfr * trend_factor * volatility),
                'loan_to_deposit_ratio': max(50, min(100, base_ltd * volatility)),
                'cash_ratio': max(3, base_cash * trend_factor * volatility)
            }
            yearly_data.append(yearly_record)
        
        data['historical_data'] = pd.DataFrame(yearly_data)
        
        # Add institution metadata
        data['institution_name'] = institution
        data['institution_type'] = "Bank" if "Bank" in institution else "Broker Dealer"
        data['assets'] = base_rwa * np.random.uniform(3, 8)  # Total assets estimate
        data['employees'] = int(np.random.uniform(50000, 250000))
        data['branches'] = int(np.random.uniform(1000, 5000)) if "Bank" in institution else int(np.random.uniform(100, 500))
        
        bank_data[institution] = data
    
    return bank_data

def get_metric_info():
    """Return information about financial metrics for display purposes."""
    return {
        'capitalization': {
            'capital_adequacy_ratio': {
                'name': 'Capital Adequacy Ratio',
                'unit': '%',
                'description': 'Measures bank\'s available capital as percentage of risk-weighted assets',
                'benchmark': {'good': 12, 'fair': 10, 'poor': 8}
            },
            'tier1_ratio': {
                'name': 'Tier 1 Capital Ratio', 
                'unit': '%',
                'description': 'Core capital ratio measuring financial strength',
                'benchmark': {'good': 10, 'fair': 8, 'poor': 6}
            },
            'leverage_ratio': {
                'name': 'Leverage Ratio',
                'unit': '%', 
                'description': 'Tier 1 capital as percentage of total assets',
                'benchmark': {'good': 5, 'fair': 4, 'poor': 3}
            },
            'risk_weighted_assets': {
                'name': 'Risk Weighted Assets',
                'unit': '$ Millions',
                'description': 'Total assets adjusted for credit risk',
                'benchmark': {'good': None, 'fair': None, 'poor': None}
            }
        },
        'asset_quality': {
            'npl_ratio': {
                'name': 'Non-Performing Loans Ratio',
                'unit': '%',
                'description': 'Percentage of loans that are non-performing',
                'benchmark': {'good': 1, 'fair': 2, 'poor': 3}
            },
            'loan_loss_provisions': {
                'name': 'Loan Loss Provisions',
                'unit': '%',
                'description': 'Provisions set aside for expected loan losses',
                'benchmark': {'good': 0.5, 'fair': 1.0, 'poor': 1.5}
            },
            'coverage_ratio': {
                'name': 'Coverage Ratio',
                'unit': '%',
                'description': 'Provisions as percentage of non-performing loans',
                'benchmark': {'good': 80, 'fair': 60, 'poor': 40}
            },
            'asset_classification': {
                'name': 'Asset Classification Score',
                'unit': 'Score',
                'description': 'Overall asset quality classification score',
                'benchmark': {'good': 2, 'fair': 4, 'poor': 6}
            }
        },
        'profitability': {
            'return_on_assets': {
                'name': 'Return on Assets (ROA)',
                'unit': '%',
                'description': 'Net income as percentage of total assets',
                'benchmark': {'good': 1.2, 'fair': 0.8, 'poor': 0.4}
            },
            'return_on_equity': {
                'name': 'Return on Equity (ROE)',
                'unit': '%',
                'description': 'Net income as percentage of shareholders\' equity',
                'benchmark': {'good': 12, 'fair': 8, 'poor': 4}
            },
            'net_interest_margin': {
                'name': 'Net Interest Margin',
                'unit': '%',
                'description': 'Net interest income as percentage of earning assets',
                'benchmark': {'good': 3.5, 'fair': 2.5, 'poor': 1.5}
            },
            'cost_to_income_ratio': {
                'name': 'Cost-to-Income Ratio',
                'unit': '%',
                'description': 'Operating expenses as percentage of operating income',
                'benchmark': {'good': 60, 'fair': 70, 'poor': 80}
            },
            'earnings_per_share': {
                'name': 'Earnings Per Share',
                'unit': '$',
                'description': 'Net earnings divided by number of shares outstanding',
                'benchmark': {'good': 8, 'fair': 5, 'poor': 2}
            }
        },
        'liquidity': {
            'liquidity_coverage_ratio': {
                'name': 'Liquidity Coverage Ratio (LCR)',
                'unit': '%',
                'description': 'High-quality liquid assets vs net cash outflows',
                'benchmark': {'good': 120, 'fair': 110, 'poor': 100}
            },
            'net_stable_funding_ratio': {
                'name': 'Net Stable Funding Ratio (NSFR)',
                'unit': '%',
                'description': 'Stable funding vs required stable funding',
                'benchmark': {'good': 110, 'fair': 105, 'poor': 100}
            },
            'loan_to_deposit_ratio': {
                'name': 'Loan-to-Deposit Ratio',
                'unit': '%',
                'description': 'Total loans as percentage of total deposits',
                'benchmark': {'good': 80, 'fair': 85, 'poor': 90}
            },
            'cash_ratio': {
                'name': 'Cash Ratio',
                'unit': '%',
                'description': 'Cash and equivalents as percentage of current liabilities',
                'benchmark': {'good': 10, 'fair': 7, 'poor': 5}
            }
        }
    }
