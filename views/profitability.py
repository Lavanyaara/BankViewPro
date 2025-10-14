import streamlit as st
import plotly.graph_objects as go
import numpy as np
from utils.commentary_generator import generate_metric_commentary, generate_section_commentary
from utils.data_generator import get_metric_info

def render_profitability(bank_data, institution_name):
    """Render the Profitability tab with earnings and efficiency metrics."""
    
    st.header("💵 Profitability Analysis")
    
    # Get historical data
    historical_data = bank_data['historical_data']
    latest_data = historical_data.iloc[-1]
    
    # Get metric information
    metric_info = get_metric_info()['profitability']
    
    # Key profitability metrics
    profit_metrics = [
        'return_on_assets',
        'return_on_equity',
        'net_interest_margin',
        'cost_to_income_ratio',
        'earnings_per_share'
    ]
    
    # Display current metrics
    st.subheader("Current Profitability Metrics")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        prev_roa = historical_data.iloc[-2]['return_on_assets']
        delta_roa = latest_data['return_on_assets'] - prev_roa
        st.metric(
            "Return on Assets",
            f"{latest_data['return_on_assets']:.2f}%",
            delta=f"{delta_roa:.2f}%"
        )
    
    with col2:
        prev_roe = historical_data.iloc[-2]['return_on_equity']
        delta_roe = latest_data['return_on_equity'] - prev_roe
        st.metric(
            "Return on Equity",
            f"{latest_data['return_on_equity']:.2f}%",
            delta=f"{delta_roe:.2f}%"
        )
    
    with col3:
        prev_nim = historical_data.iloc[-2]['net_interest_margin']
        delta_nim = latest_data['net_interest_margin'] - prev_nim
        st.metric(
            "Net Interest Margin",
            f"{latest_data['net_interest_margin']:.2f}%",
            delta=f"{delta_nim:.2f}%"
        )
    
    with col4:
        prev_cir = historical_data.iloc[-2]['cost_to_income_ratio']
        delta_cir = latest_data['cost_to_income_ratio'] - prev_cir
        st.metric(
            "Cost-to-Income Ratio",
            f"{latest_data['cost_to_income_ratio']:.1f}%",
            delta=f"{delta_cir:.1f}%",
            delta_color="inverse"  # Lower is better for cost ratio
        )
    
    with col5:
        prev_eps = historical_data.iloc[-2]['earnings_per_share']
        delta_eps = latest_data['earnings_per_share'] - prev_eps
        st.metric(
            "Earnings Per Share",
            f"${latest_data['earnings_per_share']:.2f}",
            delta=f"${delta_eps:.2f}"
        )
    
    st.divider()
    
    # Detailed Metric Analysis Tabs
    st.subheader("📋 Detailed Profitability Analysis")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Return on Assets",
        "Return on Equity",
        "Net Interest Margin",
        "Cost-to-Income Ratio",
        "Earnings Per Share"
    ])
    
    with tab1:
        render_profit_metric_analysis(
            historical_data['return_on_assets'],
            'return_on_assets',
            institution_name,
            metric_info['return_on_assets']
        )
    
    with tab2:
        render_profit_metric_analysis(
            historical_data['return_on_equity'],
            'return_on_equity',
            institution_name,
            metric_info['return_on_equity']
        )
    
    with tab3:
        render_profit_metric_analysis(
            historical_data['net_interest_margin'],
            'net_interest_margin',
            institution_name,
            metric_info['net_interest_margin']
        )
    
    with tab4:
        render_profit_metric_analysis(
            historical_data['cost_to_income_ratio'],
            'cost_to_income_ratio',
            institution_name,
            metric_info['cost_to_income_ratio']
        )
    
    with tab5:
        render_profit_metric_analysis(
            historical_data['earnings_per_share'],
            'earnings_per_share',
            institution_name,
            metric_info['earnings_per_share']
        )
    
    st.divider()
    
    # Overall Profitability Commentary
    st.subheader("💬 Profitability Assessment Summary")
    
    section_data = {
        'return_on_assets': historical_data['return_on_assets'],
        'return_on_equity': historical_data['return_on_equity'],
        'net_interest_margin': historical_data['net_interest_margin'],
        'cost_to_income_ratio': historical_data['cost_to_income_ratio'],
        'earnings_per_share': historical_data['earnings_per_share']
    }
    
    with st.spinner("Generating profitability analysis..."):
        section_commentary = generate_section_commentary(
            section_data,
            "Profitability",
            institution_name
        )
    
    st.markdown(f"""
    <div style="background-color: #e8f5e8; padding: 15px; border-radius: 8px; margin: 10px 0;">
    <h4 style="margin-top: 0;">Profitability Summary</h4>
    <p style="font-size: 15px; line-height: 1.5; margin-bottom: 0;">{section_commentary}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Industry Benchmarks Context
    st.subheader("🏭 Industry Context & Peer Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Industry Benchmarks (US Banks):**
        - **Excellent ROA:** > 1.2%
        - **Good ROA:** 0.8% - 1.2%
        - **Excellent ROE:** > 12%
        - **Good ROE:** 8% - 12%
        - **Good NIM:** > 3.5%
        """)
    
    with col2:
        st.markdown("""
        **Efficiency Standards:**
        - **Excellent C/I Ratio:** < 60%
        - **Good C/I Ratio:** 60% - 70%
        - **Poor C/I Ratio:** > 80%
        - **Peer Group:** Large Regional Banks
        """)

def render_profit_metric_analysis(metric_data, metric_name, institution_name, metric_info):
    """Render detailed analysis for a specific profitability metric."""
    
    current_value = metric_data.iloc[-1]
    historical_avg = metric_data.mean()
    volatility = metric_data.std()
    
    # Calculate trend
    years_numeric = np.arange(len(metric_data))
    trend_coeff = np.polyfit(years_numeric, metric_data, 1)[0]
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.metric(
            f"Current {metric_info['name']}",
            f"{current_value:.2f}{metric_info['unit']}",
            delta=f"{current_value - historical_avg:.2f}{metric_info['unit']} vs avg"
        )
        
        st.markdown(f"**5-Year Average:** {historical_avg:.2f}{metric_info['unit']}")
        st.markdown(f"**Volatility:** {volatility:.2f}{metric_info['unit']}")
        st.markdown(f"**Annual Trend:** {trend_coeff:.3f}{metric_info['unit']}")
        
        # Performance grade
        benchmark = metric_info['benchmark']
        if benchmark['good'] is not None:
            if 'cost' in metric_name.lower():  # Cost ratios - lower is better
                if current_value <= benchmark['good']:
                    grade = "🟢 Excellent"
                elif current_value <= benchmark['fair']:
                    grade = "🟡 Good"
                elif current_value <= benchmark['poor']:
                    grade = "🟠 Fair"
                else:
                    grade = "🔴 Poor"
            else:  # Returns and margins - higher is better
                if current_value >= benchmark['good']:
                    grade = "🟢 Excellent"
                elif current_value >= benchmark['fair']:
                    grade = "🟡 Good"
                elif current_value >= benchmark['poor']:
                    grade = "🟠 Fair"
                else:
                    grade = "🔴 Poor"
            
            st.markdown(f"**Performance Grade:** {grade}")
    
    with col2:
        # Enhanced trend chart with statistical analysis
        fig = go.Figure()
        
        # Historical data
        fig.add_trace(go.Scatter(
            x=list(range(len(metric_data))),
            y=metric_data,
            mode='lines+markers',
            name='Historical Values',
            line=dict(width=3),
            marker=dict(size=10)
        ))
        
        # Trend line
        trend_line = np.poly1d(np.polyfit(years_numeric, metric_data, 1))
        fig.add_trace(go.Scatter(
            x=list(range(len(metric_data))),
            y=trend_line(years_numeric),
            mode='lines',
            name='Trend Line',
            line=dict(dash='dash', color='red', width=2)
        ))
        
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
            title=f"{metric_info['name']} Analysis",
            xaxis_title="Years Ago",
            yaxis_title=f"{metric_info['name']} ({metric_info['unit']})",
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Statistical insights
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Maximum", f"{metric_data.max():.2f}{metric_info['unit']}")
    with col2:
        st.metric("Minimum", f"{metric_data.min():.2f}{metric_info['unit']}")
    with col3:
        improvement = ((current_value - metric_data.iloc[0]) / metric_data.iloc[0] * 100) if metric_data.iloc[0] != 0 else 0
        st.metric("5-Year Change", f"{improvement:.1f}%")
    
    # AI Commentary
    with st.spinner(f"Analyzing {metric_name} performance..."):
        commentary = generate_metric_commentary(
            metric_data,
            metric_name,
            institution_name,
            metric_info
        )
    
    st.markdown(f"""
    <div style="background-color: #f8f9fa; padding: 12px; border-left: 4px solid #007bff; margin: 8px 0;">
    <strong>Expert Analysis:</strong> {commentary}
    </div>
    """, unsafe_allow_html=True)

def calculate_profitability_score(latest_data):
    """Calculate overall profitability score (1-10)."""
    
    score = 0
    weights = {'roa': 0.3, 'roe': 0.3, 'nim': 0.25, 'eps': 0.15}
    
    # ROA scoring
    roa = latest_data['return_on_assets']
    if roa >= 1.2:
        roa_score = 10
    elif roa >= 0.8:
        roa_score = 5 + 5 * (roa - 0.8) / 0.4
    else:
        roa_score = max(1, 5 * roa / 0.8)
    
    # ROE scoring
    roe = latest_data['return_on_equity']
    if roe >= 12:
        roe_score = 10
    elif roe >= 8:
        roe_score = 5 + 5 * (roe - 8) / 4
    else:
        roe_score = max(1, 5 * roe / 8)
    
    # NIM scoring
    nim = latest_data['net_interest_margin']
    if nim >= 3.5:
        nim_score = 10
    elif nim >= 2.5:
        nim_score = 5 + 5 * (nim - 2.5) / 1.0
    else:
        nim_score = max(1, 5 * nim / 2.5)
    
    # EPS scoring (relative)
    eps = latest_data['earnings_per_share']
    if eps >= 8:
        eps_score = 10
    elif eps >= 5:
        eps_score = 5 + 5 * (eps - 5) / 3
    else:
        eps_score = max(1, 5 * eps / 5)
    
    score = (roa_score * weights['roa'] + roe_score * weights['roe'] + 
             nim_score * weights['nim'] + eps_score * weights['eps'])
    
    return min(10.0, max(1.0, score))

def calculate_efficiency_score(latest_data):
    """Calculate efficiency score based on cost-to-income ratio (1-10)."""
    
    cir = latest_data['cost_to_income_ratio']
    
    if cir <= 50:
        return 10.0
    elif cir <= 60:
        return 8 + 2 * (60 - cir) / 10
    elif cir <= 70:
        return 5 + 3 * (70 - cir) / 10
    elif cir <= 80:
        return 2 + 3 * (80 - cir) / 10
    else:
        return max(1.0, 2 * (90 - cir) / 10) if cir < 90 else 1.0
