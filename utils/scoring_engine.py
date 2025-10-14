import numpy as np
import pandas as pd

def calculate_overall_score(bank_data):
    """
    Calculate overall credit score based on weighted metrics across all categories.
    Score range: 1-10 (10 being best)
    
    Args:
        bank_data: Dictionary containing bank's historical data and metadata
    """
    
    # Get latest year data
    latest_data = bank_data['historical_data'].iloc[-1]
    
    # Define scoring weights for each category
    category_weights = {
        'capitalization': 0.25,
        'asset_quality': 0.30,
        'profitability': 0.25,
        'liquidity': 0.20
    }
    
    # Calculate category scores
    cap_score = calculate_capitalization_score(latest_data)
    asset_score = calculate_asset_quality_score(latest_data)
    profit_score = calculate_profitability_score(latest_data)
    liquidity_score = calculate_liquidity_score(latest_data)
    
    # Calculate weighted overall score
    overall_score = (
        cap_score * category_weights['capitalization'] +
        asset_score * category_weights['asset_quality'] +
        profit_score * category_weights['profitability'] +
        liquidity_score * category_weights['liquidity']
    )
    
    return min(10.0, max(1.0, overall_score))

def calculate_capitalization_score(data):
    """Calculate capitalization score based on capital ratios."""
    
    # Define benchmarks and weights for capitalization metrics
    metrics_config = {
        'capital_adequacy_ratio': {'weight': 0.35, 'excellent': 15, 'good': 12, 'fair': 10, 'poor': 8},
        'tier1_ratio': {'weight': 0.35, 'excellent': 12, 'good': 10, 'fair': 8, 'poor': 6},
        'leverage_ratio': {'weight': 0.30, 'excellent': 8, 'good': 6, 'fair': 5, 'poor': 3}
    }
    
    total_score = 0
    for metric, config in metrics_config.items():
        value = data[metric]
        
        # Score individual metric (1-10 scale)
        if value >= config['excellent']:
            metric_score = 10
        elif value >= config['good']:
            metric_score = 7 + 3 * (value - config['good']) / (config['excellent'] - config['good'])
        elif value >= config['fair']:
            metric_score = 5 + 2 * (value - config['fair']) / (config['good'] - config['fair'])
        elif value >= config['poor']:
            metric_score = 2 + 3 * (value - config['poor']) / (config['fair'] - config['poor'])
        else:
            metric_score = 1 + (value / config['poor']) if config['poor'] > 0 else 1
        
        total_score += metric_score * config['weight']
    
    return min(10.0, max(1.0, total_score))

def calculate_asset_quality_score(data):
    """Calculate asset quality score (lower NPL and provisions are better)."""
    
    # Define benchmarks and weights for asset quality metrics
    metrics_config = {
        'npl_ratio': {'weight': 0.40, 'excellent': 0.5, 'good': 1.0, 'fair': 2.0, 'poor': 3.0, 'reverse': True},
        'loan_loss_provisions': {'weight': 0.30, 'excellent': 0.3, 'good': 0.5, 'fair': 1.0, 'poor': 1.5, 'reverse': True},
        'coverage_ratio': {'weight': 0.20, 'excellent': 120, 'good': 100, 'fair': 80, 'poor': 60},
        'asset_classification': {'weight': 0.10, 'excellent': 1, 'good': 2, 'fair': 4, 'poor': 6, 'reverse': True}
    }
    
    total_score = 0
    for metric, config in metrics_config.items():
        value = data[metric]
        
        if config.get('reverse', False):  # Lower values are better
            if value <= config['excellent']:
                metric_score = 10
            elif value <= config['good']:
                metric_score = 7 + 3 * (config['good'] - value) / (config['good'] - config['excellent'])
            elif value <= config['fair']:
                metric_score = 5 + 2 * (config['fair'] - value) / (config['fair'] - config['good'])
            elif value <= config['poor']:
                metric_score = 2 + 3 * (config['poor'] - value) / (config['poor'] - config['fair'])
            else:
                metric_score = 1
        else:  # Higher values are better
            if value >= config['excellent']:
                metric_score = 10
            elif value >= config['good']:
                metric_score = 7 + 3 * (value - config['good']) / (config['excellent'] - config['good'])
            elif value >= config['fair']:
                metric_score = 5 + 2 * (value - config['fair']) / (config['good'] - config['fair'])
            elif value >= config['poor']:
                metric_score = 2 + 3 * (value - config['poor']) / (config['fair'] - config['poor'])
            else:
                metric_score = 1
        
        total_score += metric_score * config['weight']
    
    return min(10.0, max(1.0, total_score))

def calculate_profitability_score(data):
    """Calculate profitability score."""
    
    # Define benchmarks and weights for profitability metrics
    metrics_config = {
        'return_on_assets': {'weight': 0.25, 'excellent': 1.5, 'good': 1.2, 'fair': 0.8, 'poor': 0.4},
        'return_on_equity': {'weight': 0.25, 'excellent': 15, 'good': 12, 'fair': 8, 'poor': 4},
        'net_interest_margin': {'weight': 0.25, 'excellent': 4.0, 'good': 3.5, 'fair': 2.5, 'poor': 1.5},
        'cost_to_income_ratio': {'weight': 0.15, 'excellent': 50, 'good': 60, 'fair': 70, 'poor': 80, 'reverse': True},
        'earnings_per_share': {'weight': 0.10, 'excellent': 10, 'good': 8, 'fair': 5, 'poor': 2}
    }
    
    total_score = 0
    for metric, config in metrics_config.items():
        value = data[metric]
        
        if config.get('reverse', False):  # Lower values are better
            if value <= config['excellent']:
                metric_score = 10
            elif value <= config['good']:
                metric_score = 7 + 3 * (config['good'] - value) / (config['good'] - config['excellent'])
            elif value <= config['fair']:
                metric_score = 5 + 2 * (config['fair'] - value) / (config['fair'] - config['good'])
            elif value <= config['poor']:
                metric_score = 2 + 3 * (config['poor'] - value) / (config['poor'] - config['fair'])
            else:
                metric_score = 1
        else:  # Higher values are better
            if value >= config['excellent']:
                metric_score = 10
            elif value >= config['good']:
                metric_score = 7 + 3 * (value - config['good']) / (config['excellent'] - config['good'])
            elif value >= config['fair']:
                metric_score = 5 + 2 * (value - config['fair']) / (config['good'] - config['fair'])
            elif value >= config['poor']:
                metric_score = 2 + 3 * (value - config['poor']) / (config['fair'] - config['poor'])
            else:
                metric_score = 1
        
        total_score += metric_score * config['weight']
    
    return min(10.0, max(1.0, total_score))

def calculate_liquidity_score(data):
    """Calculate liquidity score."""
    
    # Define benchmarks and weights for liquidity metrics
    metrics_config = {
        'liquidity_coverage_ratio': {'weight': 0.35, 'excellent': 130, 'good': 120, 'fair': 110, 'poor': 100},
        'net_stable_funding_ratio': {'weight': 0.35, 'excellent': 120, 'good': 110, 'fair': 105, 'poor': 100},
        'loan_to_deposit_ratio': {'weight': 0.20, 'excellent': 75, 'good': 80, 'fair': 85, 'poor': 90, 'reverse': True},
        'cash_ratio': {'weight': 0.10, 'excellent': 12, 'good': 10, 'fair': 7, 'poor': 5}
    }
    
    total_score = 0
    for metric, config in metrics_config.items():
        value = data[metric]
        
        if config.get('reverse', False):  # Lower values are better
            if value <= config['excellent']:
                metric_score = 10
            elif value <= config['good']:
                metric_score = 7 + 3 * (config['good'] - value) / (config['good'] - config['excellent'])
            elif value <= config['fair']:
                metric_score = 5 + 2 * (config['fair'] - value) / (config['fair'] - config['good'])
            elif value <= config['poor']:
                metric_score = 2 + 3 * (config['poor'] - value) / (config['poor'] - config['fair'])
            else:
                metric_score = 1
        else:  # Higher values are better
            if value >= config['excellent']:
                metric_score = 10
            elif value >= config['good']:
                metric_score = 7 + 3 * (value - config['good']) / (config['excellent'] - config['good'])
            elif value >= config['fair']:
                metric_score = 5 + 2 * (value - config['fair']) / (config['good'] - config['fair'])
            elif value >= config['poor']:
                metric_score = 2 + 3 * (value - config['poor']) / (config['fair'] - config['poor'])
            else:
                metric_score = 1
        
        total_score += metric_score * config['weight']
    
    return min(10.0, max(1.0, total_score))

def get_score_interpretation(score):
    """Return textual interpretation of score."""
    if score >= 8.5:
        return {"rating": "AAA", "description": "Excellent Credit Quality", "color": "green"}
    elif score >= 7.5:
        return {"rating": "AA", "description": "Very Good Credit Quality", "color": "green"}
    elif score >= 6.5:
        return {"rating": "A", "description": "Good Credit Quality", "color": "blue"}
    elif score >= 5.5:
        return {"rating": "BBB", "description": "Fair Credit Quality", "color": "orange"}
    elif score >= 4.5:
        return {"rating": "BB", "description": "Speculative Credit Quality", "color": "orange"}
    elif score >= 3.5:
        return {"rating": "B", "description": "Highly Speculative", "color": "red"}
    else:
        return {"rating": "CCC", "description": "Poor Credit Quality", "color": "red"}

def calculate_category_scores(bank_data):
    """Calculate individual scores for each category."""
    latest_data = bank_data['historical_data'].iloc[-1]
    
    return {
        'capitalization': calculate_capitalization_score(latest_data),
        'asset_quality': calculate_asset_quality_score(latest_data),
        'profitability': calculate_profitability_score(latest_data),
        'liquidity': calculate_liquidity_score(latest_data)
    }
