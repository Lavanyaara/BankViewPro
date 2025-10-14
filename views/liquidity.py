import streamlit as st
import plotly.graph_objects as go
import numpy as np
from utils.commentary_generator import generate_metric_commentary, generate_section_commentary
from utils.data_generator import get_metric_info

def render_liquidity(bank_data, institution_name):
    """Render the Liquidity tab with LCR, NSFR, and other liquidity metrics."""
    
    st.header("💧 Liquidity Analysis")
    
    # Get historical data
    historical_data = bank_data['historical_data']
    latest_data = historical_data.iloc[-1]
    
    # Get metric information
    metric_info = get_metric_info()['liquidity']
    
    # Key liquidity metrics
    liquidity_metrics = [
        'liquidity_coverage_ratio',
        'net_stable_funding_ratio',
        'loan_to_deposit_ratio',
        'cash_ratio'
    ]
    
    # Display current metrics
    st.subheader("Current Liquidity Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        prev_lcr = historical_data.iloc[-2]['liquidity_coverage_ratio']
        delta_lcr = latest_data['liquidity_coverage_ratio'] - prev_lcr
        st.metric(
            "Liquidity Coverage Ratio",
            f"{latest_data['liquidity_coverage_ratio']:.1f}%",
            delta=f"{delta_lcr:.1f}%"
        )
    
    with col2:
        prev_nsfr = historical_data.iloc[-2]['net_stable_funding_ratio']
        delta_nsfr = latest_data['net_stable_funding_ratio'] - prev_nsfr
        st.metric(
            "Net Stable Funding Ratio",
            f"{latest_data['net_stable_funding_ratio']:.1f}%",
            delta=f"{delta_nsfr:.1f}%"
        )
    
    with col3:
        prev_ltd = historical_data.iloc[-2]['loan_to_deposit_ratio']
        delta_ltd = latest_data['loan_to_deposit_ratio'] - prev_ltd
        st.metric(
            "Loan-to-Deposit Ratio",
            f"{latest_data['loan_to_deposit_ratio']:.1f}%",
            delta=f"{delta_ltd:.1f}%",
            delta_color="inverse"  # Lower LTD is generally better for liquidity
        )
    
    with col4:
        prev_cash = historical_data.iloc[-2]['cash_ratio']
        delta_cash = latest_data['cash_ratio'] - prev_cash
        st.metric(
            "Cash Ratio",
            f"{latest_data['cash_ratio']:.1f}%",
            delta=f"{delta_cash:.1f}%"
        )
    
    st.divider()
    
    # Liquidity Risk Assessment
    st.subheader("⚠️ Liquidity Risk Assessment")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Liquidity stress test visualization
        st.markdown("#### Stress Test Scenario Analysis")
        
        # Calculate stress scenarios
        stress_scenarios = calculate_liquidity_stress_scenarios(latest_data)
        
        fig_stress = go.Figure()
        
        scenarios = list(stress_scenarios.keys())
        lcr_values = [stress_scenarios[s]['lcr'] for s in scenarios]
        nsfr_values = [stress_scenarios[s]['nsfr'] for s in scenarios]
        
        fig_stress.add_trace(go.Bar(
            x=scenarios,
            y=lcr_values,
            name='LCR Under Stress',
            marker_color=['green' if x >= 100 else 'red' for x in lcr_values]
        ))
        
        fig_stress.add_hline(
            y=100,
            line_dash="dash",
            line_color="red",
            annotation_text="Regulatory Minimum"
        )
        
        fig_stress.update_layout(
            title="LCR Stress Test Results",
            yaxis_title="LCR (%)",
            height=280
        )
        
        st.plotly_chart(fig_stress, use_container_width=True)
    
    with col2:
        # Liquidity risk indicators
        st.markdown("#### Liquidity Risk Indicators")
        
        risk_score = calculate_liquidity_risk_score(latest_data, historical_data)
        
        st.metric("Liquidity Risk Score", f"{risk_score:.1f}/10", 
                 help="Higher scores indicate higher liquidity risk")
        
        # Risk factor analysis
        risk_factors = assess_liquidity_risk_factors(latest_data, historical_data)
        
        st.markdown("**Risk Factors:**")
        
        for risk_level, factors in risk_factors.items():
            if factors:
                if risk_level == 'high':
                    st.markdown("🔴 **High Risk:**")
                elif risk_level == 'medium':
                    st.markdown("🟡 **Medium Risk:**")
                else:
                    st.markdown("🟢 **Low Risk:**")
                
                for factor in factors:
                    st.markdown(f"• {factor}")
        
        # Funding concentration analysis
        st.markdown("**Funding Diversification:**")
        funding_score = calculate_funding_diversification_score(latest_data)
        
        if funding_score >= 8:
            st.markdown("🟢 Well diversified funding base")
        elif funding_score >= 6:
            st.markdown("🟡 Moderately diversified funding")
        else:
            st.markdown("🔴 Concentrated funding sources")
    
    st.divider()
    
    # Liquidity Buffer Analysis
    st.subheader("🛡️ Liquidity Buffer Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Liquidity buffer composition (simulated breakdown)
        buffer_components = calculate_liquidity_buffer_composition(latest_data)
        
        fig_buffer = go.Figure(data=[
            go.Pie(
                labels=list(buffer_components.keys()),
                values=list(buffer_components.values()),
                hole=0.4,
                marker_colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
            )
        ])
        
        fig_buffer.update_layout(
            title="Liquidity Buffer Composition",
            height=300
        )
        
        st.plotly_chart(fig_buffer, use_container_width=True)
    
    with col2:
        # Liquidity runway analysis
        st.markdown("#### Liquidity Runway Analysis")
        
        runway_days = calculate_liquidity_runway(latest_data)
        
        st.metric("Estimated Liquidity Runway", f"{runway_days} days", 
                 help="Days the institution can survive without new funding")
        
        # Runway interpretation
        if runway_days > 90:
            runway_status = "🟢 Strong liquidity position"
        elif runway_days > 30:
            runway_status = "🟡 Adequate liquidity buffer"
        else:
            runway_status = "🔴 Limited liquidity runway"
        
        st.markdown(f"**Status:** {runway_status}")
        
        # Monthly cash flow projection (simplified)
        st.markdown("**Projected Monthly Cash Flow:**")
        
        cash_flow_projection = project_monthly_cash_flow(latest_data)
        
        fig_projection = go.Figure()
        
        months = list(range(1, 13))
        
        fig_projection.add_trace(go.Scatter(
            x=months,
            y=cash_flow_projection['inflows'],
            mode='lines+markers',
            name='Expected Inflows',
            line=dict(color='green', width=2)
        ))
        
        fig_projection.add_trace(go.Scatter(
            x=months,
            y=cash_flow_projection['outflows'],
            mode='lines+markers',
            name='Expected Outflows',
            line=dict(color='red', width=2)
        ))
        
        fig_projection.update_layout(
            title="12-Month Cash Flow Projection",
            xaxis_title="Month",
            yaxis_title="Cash Flow ($ Millions)",
            height=250
        )
        
        st.plotly_chart(fig_projection, use_container_width=True)
    
    st.divider()
    
    # Detailed Metric Analysis Tabs
    st.subheader("📋 Detailed Liquidity Metric Analysis")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "Liquidity Coverage Ratio",
        "Net Stable Funding Ratio",
        "Loan-to-Deposit Ratio",
        "Cash Ratio"
    ])
    
    with tab1:
        render_liquidity_metric_analysis(
            historical_data['liquidity_coverage_ratio'],
            'liquidity_coverage_ratio',
            institution_name,
            metric_info['liquidity_coverage_ratio']
        )
    
    with tab2:
        render_liquidity_metric_analysis(
            historical_data['net_stable_funding_ratio'],
            'net_stable_funding_ratio',
            institution_name,
            metric_info['net_stable_funding_ratio']
        )
    
    with tab3:
        render_liquidity_metric_analysis(
            historical_data['loan_to_deposit_ratio'],
            'loan_to_deposit_ratio',
            institution_name,
            metric_info['loan_to_deposit_ratio']
        )
    
    with tab4:
        render_liquidity_metric_analysis(
            historical_data['cash_ratio'],
            'cash_ratio',
            institution_name,
            metric_info['cash_ratio']
        )
    
    st.divider()
    
    # Overall Liquidity Commentary
    st.subheader("💬 Liquidity Assessment Summary")
    
    section_data = {
        'liquidity_coverage_ratio': historical_data['liquidity_coverage_ratio'],
        'net_stable_funding_ratio': historical_data['net_stable_funding_ratio'],
        'loan_to_deposit_ratio': historical_data['loan_to_deposit_ratio'],
        'cash_ratio': historical_data['cash_ratio']
    }
    
    with st.spinner("Generating liquidity analysis..."):
        section_commentary = generate_section_commentary(
            section_data,
            "Liquidity",
            institution_name
        )
    
    st.markdown(f"""
    <div style="background-color: #e1f5fe; padding: 15px; border-radius: 8px; margin: 10px 0;">
    <h4 style="margin-top: 0;">Liquidity Summary</h4>
    <p style="font-size: 15px; line-height: 1.5; margin-bottom: 0;">{section_commentary}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Regulatory Framework Context
    st.subheader("📋 Regulatory Framework & Requirements")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Basel III Liquidity Requirements:**
        - **LCR Minimum:** 100% (since 2019)
        - **NSFR Minimum:** 100% (since 2021)
        - **Additional Buffer:** Often required by supervisors
        - **Reporting Frequency:** Monthly for large banks
        """)
        
        st.markdown("""
        **US Implementation:**
        - **Enhanced Prudential Standards:** Banks >$100B
        - **Stress Testing:** Liquidity stress scenarios
        - **Resolution Planning:** Living wills requirement
        """)
    
    with col2:
        st.markdown("""
        **Key Liquidity Principles:**
        - **Diversified Funding:** Avoid concentration risk
        - **Maturity Matching:** Align asset-liability maturities  
        - **Contingency Planning:** Access to emergency funding
        - **Early Warning Indicators:** Proactive monitoring
        """)
        
        st.markdown("""
        **Market Access Considerations:**
        - **Credit Rating Impact:** On funding costs
        - **Collateral Quality:** For secured funding
        - **Counterparty Limits:** Funding source constraints
        """)

def render_liquidity_metric_analysis(metric_data, metric_name, institution_name, metric_info):
    """Render detailed analysis for a specific liquidity metric."""
    
    current_value = metric_data.iloc[-1]
    historical_avg = metric_data.mean()
    volatility = metric_data.std()
    
    # Calculate regulatory compliance
    if metric_name in ['liquidity_coverage_ratio', 'net_stable_funding_ratio']:
        compliance_status = "✅ Compliant" if current_value >= 100 else "❌ Non-Compliant"
        buffer = current_value - 100
    else:
        compliance_status = "N/A"
        buffer = None
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.metric(
            f"Current {metric_info['name']}",
            f"{current_value:.1f}{metric_info['unit']}",
            delta=f"{current_value - historical_avg:.1f}{metric_info['unit']} vs avg"
        )
        
        if buffer is not None:
            st.metric("Regulatory Buffer", f"{buffer:.1f}%")
        
        st.markdown(f"**Regulatory Status:** {compliance_status}")
        st.markdown(f"**5-Year Volatility:** {volatility:.1f}{metric_info['unit']}")
        st.markdown(f"**Description:** {metric_info['description']}")
        
        # Performance assessment
        benchmark = metric_info['benchmark']
        if benchmark['good'] is not None:
            if 'loan_to_deposit' in metric_name.lower():  # Lower is better for LTD
                if current_value <= benchmark['good']:
                    performance = "🟢 Excellent"
                elif current_value <= benchmark['fair']:
                    performance = "🟡 Good"
                elif current_value <= benchmark['poor']:
                    performance = "🟠 Fair"
                else:
                    performance = "🔴 Poor"
            else:  # Higher is better for other liquidity ratios
                if current_value >= benchmark['good']:
                    performance = "🟢 Excellent"
                elif current_value >= benchmark['fair']:
                    performance = "🟡 Good"
                elif current_value >= benchmark['poor']:
                    performance = "🟠 Fair"
                else:
                    performance = "🔴 Poor"
            
            st.markdown(f"**Performance Rating:** {performance}")
    
    with col2:
        # Enhanced trend chart with regulatory minimum
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=list(range(len(metric_data))),
            y=metric_data,
            mode='lines+markers',
            name=metric_info['name'],
            line=dict(width=3),
            marker=dict(size=10),
            fill='tonexty'
        ))
        
        # Add regulatory minimum for LCR and NSFR
        if metric_name in ['liquidity_coverage_ratio', 'net_stable_funding_ratio']:
            fig.add_hline(
                y=100,
                line_dash="dash",
                line_color="red",
                annotation_text="Regulatory Minimum (100%)"
            )
        
        # Add benchmark lines
        if metric_info['benchmark']['good'] is not None:
            fig.add_hline(
                y=metric_info['benchmark']['good'],
                line_dash="dot",
                line_color="green",
                annotation_text="Good Threshold"
            )
            fig.add_hline(
                y=metric_info['benchmark']['fair'],
                line_dash="dot",
                line_color="orange",
                annotation_text="Fair Threshold"
            )
        
        fig.update_layout(
            title=f"{metric_info['name']} Historical Trend",
            xaxis_title="Years Ago",
            yaxis_title=f"{metric_info['name']} ({metric_info['unit']})",
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Statistical analysis
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("5-Year High", f"{metric_data.max():.1f}{metric_info['unit']}")
    with col2:
        st.metric("5-Year Low", f"{metric_data.min():.1f}{metric_info['unit']}")
    with col3:
        trend_change = metric_data.iloc[-1] - metric_data.iloc[0]
        st.metric("5-Year Change", f"{trend_change:+.1f}{metric_info['unit']}")
    
    # AI Commentary
    with st.spinner(f"Analyzing {metric_name} trends..."):
        commentary = generate_metric_commentary(
            metric_data,
            metric_name,
            institution_name,
            metric_info
        )
    
    st.markdown(f"""
    <div style="background-color: #f8f9fa; padding: 12px; border-left: 4px solid #17a2b8; margin: 8px 0;">
    <strong>Expert Analysis:</strong> {commentary}
    </div>
    """, unsafe_allow_html=True)

def calculate_liquidity_stress_scenarios(latest_data):
    """Calculate liquidity ratios under various stress scenarios."""
    
    base_lcr = latest_data['liquidity_coverage_ratio']
    base_nsfr = latest_data['net_stable_funding_ratio']
    
    scenarios = {
        'Baseline': {'lcr': base_lcr, 'nsfr': base_nsfr},
        'Mild Stress': {
            'lcr': base_lcr * 0.85,  # 15% decline in liquid assets
            'nsfr': base_nsfr * 0.90   # 10% decline in stable funding
        },
        'Moderate Stress': {
            'lcr': base_lcr * 0.70,  # 30% decline
            'nsfr': base_nsfr * 0.80   # 20% decline
        },
        'Severe Stress': {
            'lcr': base_lcr * 0.55,  # 45% decline
            'nsfr': base_nsfr * 0.70   # 30% decline
        }
    }
    
    return scenarios

def calculate_liquidity_risk_score(latest_data, historical_data):
    """Calculate liquidity risk score (1-10, higher = more risk)."""
    
    risk_score = 5.0  # Base neutral score
    
    # LCR assessment
    lcr = latest_data['liquidity_coverage_ratio']
    if lcr < 100:
        risk_score += 3.0  # Major penalty for non-compliance
    elif lcr < 110:
        risk_score += 1.0
    elif lcr > 130:
        risk_score -= 1.0
    
    # NSFR assessment  
    nsfr = latest_data['net_stable_funding_ratio']
    if nsfr < 100:
        risk_score += 2.0
    elif nsfr < 105:
        risk_score += 0.5
    elif nsfr > 120:
        risk_score -= 0.5
    
    # Loan-to-deposit ratio assessment
    ltd = latest_data['loan_to_deposit_ratio']
    if ltd > 95:
        risk_score += 1.5
    elif ltd > 90:
        risk_score += 0.5
    elif ltd < 80:
        risk_score -= 0.5
    
    # Volatility assessment
    lcr_volatility = historical_data['liquidity_coverage_ratio'].std()
    if lcr_volatility > 10:
        risk_score += 0.5
    
    return min(10.0, max(1.0, risk_score))

def assess_liquidity_risk_factors(latest_data, historical_data):
    """Assess various liquidity risk factors."""
    
    risk_factors = {'high': [], 'medium': [], 'low': []}
    
    # Regulatory compliance
    if latest_data['liquidity_coverage_ratio'] < 100:
        risk_factors['high'].append("LCR below regulatory minimum")
    elif latest_data['liquidity_coverage_ratio'] > 120:
        risk_factors['low'].append("Strong LCR buffer above minimum")
    else:
        risk_factors['medium'].append("LCR meets but close to minimum")
    
    if latest_data['net_stable_funding_ratio'] < 100:
        risk_factors['high'].append("NSFR below regulatory minimum")
    elif latest_data['net_stable_funding_ratio'] > 110:
        risk_factors['low'].append("Strong NSFR buffer")
    else:
        risk_factors['medium'].append("NSFR adequate but limited buffer")
    
    # Funding concentration
    if latest_data['loan_to_deposit_ratio'] > 90:
        risk_factors['high'].append("High loan-to-deposit ratio")
    elif latest_data['loan_to_deposit_ratio'] < 80:
        risk_factors['low'].append("Conservative lending relative to deposits")
    else:
        risk_factors['medium'].append("Moderate loan-to-deposit ratio")
    
    # Cash position
    if latest_data['cash_ratio'] < 5:
        risk_factors['high'].append("Low cash reserves")
    elif latest_data['cash_ratio'] > 10:
        risk_factors['low'].append("Strong cash position")
    else:
        risk_factors['medium'].append("Adequate cash reserves")
    
    # Trend analysis
    lcr_trend = latest_data['liquidity_coverage_ratio'] - historical_data['liquidity_coverage_ratio'].iloc[0]
    if lcr_trend < -10:
        risk_factors['high'].append("Declining LCR trend")
    elif lcr_trend > 10:
        risk_factors['low'].append("Improving LCR trend")
    
    return risk_factors

def calculate_funding_diversification_score(latest_data):
    """Calculate funding diversification score based on deposit ratios."""
    
    # Simplified scoring based on loan-to-deposit ratio
    # Lower LTD suggests more diversified funding sources
    ltd = latest_data['loan_to_deposit_ratio']
    
    if ltd < 75:
        return 9.0  # Highly diversified
    elif ltd < 85:
        return 7.0  # Well diversified
    elif ltd < 95:
        return 5.0  # Moderately diversified
    else:
        return 3.0  # Concentrated funding

def calculate_liquidity_buffer_composition(latest_data):
    """Calculate estimated liquidity buffer composition."""
    
    # Simplified breakdown based on typical bank composition
    total_buffer = latest_data['liquidity_coverage_ratio']
    
    return {
        'Cash & Central Bank Reserves': total_buffer * 0.30,
        'Government Securities': total_buffer * 0.25,
        'Corporate Bonds (High Grade)': total_buffer * 0.20,
        'Covered Bonds': total_buffer * 0.15,
        'Other Liquid Assets': total_buffer * 0.10
    }

def calculate_liquidity_runway(latest_data):
    """Calculate estimated liquidity runway in days."""
    
    # Simplified calculation based on cash ratio and operational needs
    cash_ratio = latest_data['cash_ratio']
    lcr = latest_data['liquidity_coverage_ratio']
    
    # Estimate based on liquidity position
    base_runway = 30  # Base 30 days
    
    # Adjust based on LCR
    if lcr > 130:
        lcr_adjustment = 60
    elif lcr > 110:
        lcr_adjustment = 30
    elif lcr > 100:
        lcr_adjustment = 0
    else:
        lcr_adjustment = -30
    
    # Adjust based on cash ratio
    cash_adjustment = (cash_ratio - 8) * 5  # 5 days per percentage point above/below 8%
    
    runway = base_runway + lcr_adjustment + cash_adjustment
    return max(7, min(180, int(runway)))  # Cap between 7 and 180 days

def project_monthly_cash_flow(latest_data):
    """Project monthly cash flows for the next 12 months."""
    
    # Simplified projection based on current ratios
    base_inflow = 100  # Base monthly inflow in millions
    base_outflow = 95   # Base monthly outflow in millions
    
    # Seasonal and trend adjustments
    seasonal_factors = [0.9, 0.95, 1.0, 1.05, 1.0, 0.95, 0.9, 0.95, 1.05, 1.1, 1.05, 1.0]
    
    inflows = [base_inflow * factor for factor in seasonal_factors]
    outflows = [base_outflow * factor for factor in seasonal_factors]
    
    return {
        'inflows': inflows,
        'outflows': outflows
    }
