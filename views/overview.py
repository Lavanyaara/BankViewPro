import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from utils.chart_generator import create_performance_radar, create_comparison_bar_chart
from utils.commentary_generator import generate_overall_commentary
from utils.scoring_engine import calculate_category_scores, get_score_interpretation
from utils.data_generator import get_metric_info

def render_overview(bank_data, institution_name):
    """Render the Overview tab with consolidated metrics and scoring."""
    
    st.header("🏦 Executive Overview")
    
    # Get latest year data
    latest_data = bank_data['historical_data'].iloc[-1]
    
    # Calculate category scores
    category_scores = calculate_category_scores(bank_data)
    overall_score = sum(category_scores.values()) / len(category_scores)
    
    # Score interpretation
    score_info = get_score_interpretation(overall_score)
    
    # Top metrics display
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Overall Score",
            f"{overall_score:.1f}/10.0",
            delta=None
        )
        st.markdown(f"**Rating:** {score_info['rating']}")
        st.markdown(f"*{score_info['description']}*")
    
    with col2:
        st.metric(
            "Capital Adequacy",
            f"{latest_data['capital_adequacy_ratio']:.1f}%",
            delta=f"{latest_data['capital_adequacy_ratio'] - bank_data['historical_data'].iloc[-2]['capital_adequacy_ratio']:.1f}%"
        )
    
    with col3:
        st.metric(
            "NPL Ratio",
            f"{latest_data['npl_ratio']:.2f}%",
            delta=f"{latest_data['npl_ratio'] - bank_data['historical_data'].iloc[-2]['npl_ratio']:.2f}%"
        )
    
    with col4:
        st.metric(
            "Return on Assets",
            f"{latest_data['return_on_assets']:.2f}%",
            delta=f"{latest_data['return_on_assets'] - bank_data['historical_data'].iloc[-2]['return_on_assets']:.2f}%"
        )
    
    st.divider()
    
    # Institution Information
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Institution Profile")
        st.write(f"**Name:** {institution_name}")
        st.write(f"**Type:** {bank_data.get('institution_type', 'Bank')}")
        st.write(f"**Total Assets:** ${bank_data.get('assets', 0):,.0f}M")
        st.write(f"**Employees:** {bank_data.get('employees', 0):,}")
        if bank_data.get('branches'):
            st.write(f"**Branches:** {bank_data.get('branches', 0):,}")
    
    with col2:
        st.subheader("Category Performance Scores")
        
        # Create category scores chart
        categories = list(category_scores.keys())
        scores = list(category_scores.values())
        
        fig_scores = go.Figure()
        
        # Color code based on score - using new theme colors
        colors = []
        for score in scores:
            if score >= 7.5:
                colors.append('#355E3B')  # Hunter Green
            elif score >= 6.0:
                colors.append('#98D8C8')  # Mint
            elif score >= 4.5:
                colors.append('#FF8C42')  # Orange
            else:
                colors.append('#F7B32B')  # Yellow (warning)
        
        fig_scores.add_trace(go.Bar(
            x=[cat.title() for cat in categories],
            y=scores,
            marker_color=colors,
            text=[f"{score:.1f}" for score in scores],
            textposition='auto'
        ))
        
        fig_scores.update_layout(
            title="Category Scores (1-10 Scale)",
            yaxis=dict(range=[0, 10], title="Score"),
            xaxis_title="Category",
            height=300,
            showlegend=False
        )
        
        st.plotly_chart(fig_scores, use_container_width=True)
    
    st.divider()
    
    # Executive Summary - moved here from below
    st.subheader("📊 Executive Summary")
    
    with st.spinner("Generating comprehensive analysis..."):
        commentary = generate_overall_commentary(bank_data, institution_name, overall_score)
    
    st.markdown(f"""
    <div style="background-color: #D4E7D0; padding: 20px; border-radius: 10px; margin: 10px 0; border-left: 5px solid #355E3B;">
    <h4 style="color: #355E3B; margin-top: 0;">Credit Analysis Summary</h4>
    <p style="font-size: 16px; line-height: 1.6; color: #2A4A2E;">{commentary}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Management Quality Assessment
    st.subheader("📋 Management Quality Assessment")
    
    # Calculate management score based on trend consistency and performance
    mgmt_score = calculate_management_quality_score(bank_data['historical_data'])
    mgmt_rating = get_management_rating(mgmt_score)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.metric("Management Score", f"{mgmt_score:.1f}/10.0")
        st.markdown(f"**Rating:** {mgmt_rating['rating']}")
        st.markdown(f"*{mgmt_rating['description']}*")
    
    with col2:
        # Management assessment criteria
        st.markdown("""
        **Assessment Criteria:**
        - **Strategic Planning:** Consistency in performance improvement
        - **Risk Management:** Ability to maintain stable asset quality
        - **Operational Efficiency:** Cost management and productivity trends
        - **Capital Management:** Prudent capital allocation and planning
        """)
    
    st.divider()
    
    # Risk Assessment Matrix
    st.subheader("🎯 Risk Assessment Matrix")
    
    risk_factors = assess_risk_factors(latest_data, bank_data['historical_data'])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        for factor in risk_factors['low']:
            st.markdown(f"🟢 {factor}")
    
    with col2:
        for factor in risk_factors['medium']:
            st.markdown(f"🟡 {factor}")
    
    with col3:
        for factor in risk_factors['high']:
            st.markdown(f"🔴 {factor}")

def calculate_management_quality_score(historical_data):
    """Calculate management quality score based on performance consistency and trends."""
    
    # Factors to consider:
    # 1. Consistency in capital ratios
    # 2. Trend in asset quality
    # 3. Profitability stability
    # 4. Liquidity management
    
    score = 5.0  # Start with neutral score
    
    # Capital consistency (CAR volatility)
    car_std = historical_data['capital_adequacy_ratio'].std()
    if car_std < 1.0:
        score += 1.0
    elif car_std > 2.0:
        score -= 1.0
    
    # Asset quality trend (improving NPL is good)
    npl_trend = historical_data['npl_ratio'].iloc[-1] - historical_data['npl_ratio'].iloc[0]
    if npl_trend < -0.5:  # NPL decreased
        score += 1.5
    elif npl_trend > 0.5:  # NPL increased
        score -= 1.5
    
    # Profitability consistency (ROA volatility)
    roa_std = historical_data['return_on_assets'].std()
    if roa_std < 0.2:
        score += 1.0
    elif roa_std > 0.5:
        score -= 1.0
    
    # Liquidity management (LCR above regulatory minimum)
    avg_lcr = historical_data['liquidity_coverage_ratio'].mean()
    if avg_lcr > 120:
        score += 0.5
    elif avg_lcr < 105:
        score -= 1.0
    
    return min(10.0, max(1.0, score))

def get_management_rating(score):
    """Return management quality rating based on score."""
    if score >= 8.0:
        return {"rating": "Strong", "description": "Excellent strategic planning and execution"}
    elif score >= 6.5:
        return {"rating": "Satisfactory", "description": "Good management with consistent performance"}
    elif score >= 5.0:
        return {"rating": "Fair", "description": "Adequate management with some concerns"}
    else:
        return {"rating": "Weak", "description": "Management effectiveness needs improvement"}

def assess_risk_factors(latest_data, historical_data):
    """Assess various risk factors and categorize them."""
    
    risk_factors = {'low': [], 'medium': [], 'high': []}
    
    # Capital risk
    if latest_data['capital_adequacy_ratio'] > 15:
        risk_factors['low'].append("Strong capital position")
    elif latest_data['capital_adequacy_ratio'] < 10:
        risk_factors['high'].append("Weak capital adequacy")
    else:
        risk_factors['medium'].append("Adequate capital levels")
    
    # Asset quality risk
    if latest_data['npl_ratio'] < 1.0:
        risk_factors['low'].append("Excellent asset quality")
    elif latest_data['npl_ratio'] > 3.0:
        risk_factors['high'].append("Poor asset quality")
    else:
        risk_factors['medium'].append("Moderate asset quality concerns")
    
    # Profitability risk
    if latest_data['return_on_assets'] > 1.2:
        risk_factors['low'].append("Strong profitability")
    elif latest_data['return_on_assets'] < 0.5:
        risk_factors['high'].append("Weak profitability")
    else:
        risk_factors['medium'].append("Moderate profitability")
    
    # Liquidity risk
    if latest_data['liquidity_coverage_ratio'] > 130:
        risk_factors['low'].append("Strong liquidity position")
    elif latest_data['liquidity_coverage_ratio'] < 110:
        risk_factors['high'].append("Tight liquidity position")
    else:
        risk_factors['medium'].append("Adequate liquidity levels")
    
    # Trend analysis
    roa_trend = latest_data['return_on_assets'] - historical_data['return_on_assets'].iloc[0]
    if roa_trend > 0.3:
        risk_factors['low'].append("Improving profitability trend")
    elif roa_trend < -0.3:
        risk_factors['high'].append("Declining profitability trend")
    
    return risk_factors
