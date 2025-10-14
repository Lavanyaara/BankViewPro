import streamlit as st
import plotly.graph_objects as go
import numpy as np
from utils.chart_generator import create_trend_chart, create_metric_gauge, create_correlation_heatmap
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
    
    # Profitability Trends Overview
    st.subheader("📈 Profitability Trends Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Returns chart (ROA and ROE)
        fig_returns = go.Figure()
        
        fig_returns.add_trace(go.Scatter(
            x=historical_data['year'],
            y=historical_data['return_on_assets'],
            mode='lines+markers',
            name='Return on Assets (%)',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=8),
            yaxis='y'
        ))
        
        fig_returns.add_trace(go.Scatter(
            x=historical_data['year'],
            y=historical_data['return_on_equity'],
            mode='lines+markers',
            name='Return on Equity (%)',
            line=dict(color='#ff7f0e', width=3),
            marker=dict(size=8),
            yaxis='y2'
        ))
        
        fig_returns.update_layout(
            title="Return Metrics Trend",
            xaxis_title="Year",
            yaxis=dict(title="ROA (%)", side='left', color='#1f77b4'),
            yaxis2=dict(title="ROE (%)", side='right', overlaying='y', color='#ff7f0e'),
            height=400,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_returns, use_container_width=True)
    
    with col2:
        # Efficiency and Margin chart
        fig_efficiency = go.Figure()
        
        fig_efficiency.add_trace(go.Scatter(
            x=historical_data['year'],
            y=historical_data['net_interest_margin'],
            mode='lines+markers',
            name='Net Interest Margin',
            line=dict(color='#2ca02c', width=3),
            marker=dict(size=8),
            yaxis='y'
        ))
        
        fig_efficiency.add_trace(go.Scatter(
            x=historical_data['year'],
            y=historical_data['cost_to_income_ratio'],
            mode='lines+markers',
            name='Cost-to-Income Ratio',
            line=dict(color='#d62728', width=3),
            marker=dict(size=8),
            yaxis='y2'
        ))
        
        fig_efficiency.update_layout(
            title="Efficiency & Margin Trends",
            xaxis_title="Year",
            yaxis=dict(title="NIM (%)", side='left', color='#2ca02c'),
            yaxis2=dict(title="C/I Ratio (%)", side='right', overlaying='y', color='#d62728'),
            height=400,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_efficiency, use_container_width=True)
    
    st.divider()
    
    # Performance Gauges
    st.subheader("🎯 Current Performance vs Industry Benchmarks")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # ROA Gauge
        roa_info = metric_info['return_on_assets']
        fig_roa_gauge = create_metric_gauge(
            latest_data['return_on_assets'],
            roa_info['benchmark']['good'],
            roa_info['benchmark']['fair'],
            "Return on Assets",
            "%"
        )
        st.plotly_chart(fig_roa_gauge, use_container_width=True)
    
    with col2:
        # ROE Gauge
        roe_info = metric_info['return_on_equity']
        fig_roe_gauge = create_metric_gauge(
            latest_data['return_on_equity'],
            roe_info['benchmark']['good'],
            roe_info['benchmark']['fair'],
            "Return on Equity",
            "%"
        )
        st.plotly_chart(fig_roe_gauge, use_container_width=True)
    
    with col3:
        # Net Interest Margin Gauge
        nim_info = metric_info['net_interest_margin']
        fig_nim_gauge = create_metric_gauge(
            latest_data['net_interest_margin'],
            nim_info['benchmark']['good'],
            nim_info['benchmark']['fair'],
            "Net Interest Margin",
            "%"
        )
        st.plotly_chart(fig_nim_gauge, use_container_width=True)
    
    st.divider()
    
    # Profitability Analysis Deep Dive
    st.subheader("🔍 Profitability Deep Dive")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Earnings per Share trend with additional analysis
        fig_eps = go.Figure()
        
        fig_eps.add_trace(go.Scatter(
            x=historical_data['year'],
            y=historical_data['earnings_per_share'],
            mode='lines+markers',
            name='Earnings Per Share',
            line=dict(color='#9467bd', width=4),
            marker=dict(size=10),
            fill='tonexty'
        ))
        
        # Add trend line
        years_numeric = np.arange(len(historical_data))
        eps_trend = np.polyfit(years_numeric, historical_data['earnings_per_share'], 1)
        trend_line = np.poly1d(eps_trend)
        
        fig_eps.add_trace(go.Scatter(
            x=historical_data['year'],
            y=trend_line(years_numeric),
            mode='lines',
            name='Trend Line',
            line=dict(color='red', dash='dash', width=2)
        ))
        
        fig_eps.update_layout(
            title="Earnings Per Share Trend & Projection",
            xaxis_title="Year",
            yaxis_title="EPS ($)",
            height=400
        )
        
        st.plotly_chart(fig_eps, use_container_width=True)
    
    with col2:
        # Profitability efficiency matrix
        st.markdown("#### Profitability Efficiency Analysis")
        
        # Calculate profitability score
        profit_score = calculate_profitability_score(latest_data)
        efficiency_score = calculate_efficiency_score(latest_data)
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Profitability Score", f"{profit_score:.1f}/10")
        with col_b:
            st.metric("Efficiency Score", f"{efficiency_score:.1f}/10")
        
        # Profitability matrix visualization
        fig_matrix = go.Figure()
        
        fig_matrix.add_trace(go.Scatter(
            x=[efficiency_score],
            y=[profit_score],
            mode='markers',
            name=institution_name,
            marker=dict(size=20, color='red'),
            text=[institution_name],
            textposition="top center"
        ))
        
        # Add quadrant background
        fig_matrix.add_shape(type="rect", x0=0, y0=5, x1=5, y1=10, fillcolor="rgba(255,0,0,0.1)")
        fig_matrix.add_shape(type="rect", x0=5, y0=5, x1=10, y1=10, fillcolor="rgba(255,255,0,0.1)")  
        fig_matrix.add_shape(type="rect", x0=0, y0=0, x1=5, y1=5, fillcolor="rgba(255,165,0,0.1)")
        fig_matrix.add_shape(type="rect", x0=5, y0=0, x1=10, y1=5, fillcolor="rgba(0,128,0,0.1)")
        
        fig_matrix.update_layout(
            title="Profitability vs Efficiency Matrix",
            xaxis=dict(title="Efficiency Score", range=[0, 10]),
            yaxis=dict(title="Profitability Score", range=[0, 10]),
            height=400
        )
        
        st.plotly_chart(fig_matrix, use_container_width=True)
        
        # Quadrant interpretation
        if profit_score >= 5 and efficiency_score >= 5:
            quadrant = "🟢 High Profit, High Efficiency"
        elif profit_score >= 5 and efficiency_score < 5:
            quadrant = "🟡 High Profit, Low Efficiency"
        elif profit_score < 5 and efficiency_score >= 5:
            quadrant = "🟠 Low Profit, High Efficiency"
        else:
            quadrant = "🔴 Low Profit, Low Efficiency"
        
        st.markdown(f"**Position:** {quadrant}")
    
    st.divider()
    
    # Profitability correlation analysis
    st.subheader("📊 Profitability Correlation Analysis")
    
    correlation_metrics = ['return_on_assets', 'return_on_equity', 'net_interest_margin', 'cost_to_income_ratio']
    fig_corr = create_correlation_heatmap(
        historical_data,
        correlation_metrics,
        "Profitability Metrics Correlation Matrix"
    )
    st.plotly_chart(fig_corr, use_container_width=True)
    
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
    <div style="background-color: #e8f5e8; padding: 20px; border-radius: 10px; margin: 10px 0;">
    <h4>Profitability Summary</h4>
    <p style="font-size: 16px; line-height: 1.6;">{section_commentary}</p>
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
            height=400
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
    <div style="background-color: #f8f9fa; padding: 15px; border-left: 4px solid #007bff; margin: 10px 0;">
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
