import streamlit as st
import plotly.graph_objects as go
from utils.chart_generator import create_trend_chart, create_metric_gauge
from utils.commentary_generator import generate_metric_commentary, generate_section_commentary
from utils.data_generator import get_metric_info

def render_capitalization(bank_data, institution_name):
    """Render the Capitalization tab with capital adequacy metrics."""
    
    st.header("💰 Capitalization Analysis")
    
    # Get historical data
    historical_data = bank_data['historical_data']
    latest_data = historical_data.iloc[-1]
    
    # Get metric information
    metric_info = get_metric_info()['capitalization']
    
    # Key capitalization metrics
    cap_metrics = [
        'capital_adequacy_ratio',
        'tier1_ratio', 
        'leverage_ratio',
        'risk_weighted_assets'
    ]
    
    # Display current metrics
    st.subheader("Current Capitalization Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        prev_car = historical_data.iloc[-2]['capital_adequacy_ratio']
        st.metric(
            "Capital Adequacy Ratio",
            f"{latest_data['capital_adequacy_ratio']:.2f}%",
            delta=f"{latest_data['capital_adequacy_ratio'] - prev_car:.2f}%"
        )
    
    with col2:
        prev_tier1 = historical_data.iloc[-2]['tier1_ratio']
        st.metric(
            "Tier 1 Capital Ratio", 
            f"{latest_data['tier1_ratio']:.2f}%",
            delta=f"{latest_data['tier1_ratio'] - prev_tier1:.2f}%"
        )
    
    with col3:
        prev_leverage = historical_data.iloc[-2]['leverage_ratio']
        st.metric(
            "Leverage Ratio",
            f"{latest_data['leverage_ratio']:.2f}%", 
            delta=f"{latest_data['leverage_ratio'] - prev_leverage:.2f}%"
        )
    
    with col4:
        prev_rwa = historical_data.iloc[-2]['risk_weighted_assets']
        st.metric(
            "Risk Weighted Assets",
            f"${latest_data['risk_weighted_assets']:,.0f}M",
            delta=f"${latest_data['risk_weighted_assets'] - prev_rwa:,.0f}M"
        )
    
    st.divider()
    
    # Detailed Metric Analysis
    st.subheader("📊 Detailed Metric Analysis")
    
    # Create tabs for each metric
    tab1, tab2, tab3, tab4 = st.tabs([
        "Capital Adequacy Ratio",
        "Tier 1 Capital Ratio", 
        "Leverage Ratio",
        "Risk Weighted Assets"
    ])
    
    with tab1:
        render_metric_analysis(
            historical_data['capital_adequacy_ratio'],
            'capital_adequacy_ratio',
            institution_name,
            metric_info['capital_adequacy_ratio']
        )
    
    with tab2:
        render_metric_analysis(
            historical_data['tier1_ratio'],
            'tier1_ratio',
            institution_name,
            metric_info['tier1_ratio']
        )
    
    with tab3:
        render_metric_analysis(
            historical_data['leverage_ratio'],
            'leverage_ratio', 
            institution_name,
            metric_info['leverage_ratio']
        )
    
    with tab4:
        render_metric_analysis(
            historical_data['risk_weighted_assets'],
            'risk_weighted_assets',
            institution_name,
            metric_info['risk_weighted_assets']
        )
    
    st.divider()
    
    # Overall Capitalization Commentary
    st.subheader("💬 Overall Capitalization Assessment")
    
    # Generate section-level commentary
    section_data = {
        'capital_adequacy_ratio': historical_data['capital_adequacy_ratio'],
        'tier1_ratio': historical_data['tier1_ratio'],
        'leverage_ratio': historical_data['leverage_ratio']
    }
    
    with st.spinner("Generating capitalization analysis..."):
        section_commentary = generate_section_commentary(
            section_data,
            "Capitalization",
            institution_name
        )
    
    st.markdown(f"""
    <div style="background-color: #e6f3ff; padding: 20px; border-radius: 10px; margin: 10px 0;">
    <h4>Capitalization Summary</h4>
    <p style="font-size: 16px; line-height: 1.6;">{section_commentary}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Regulatory Context
    st.subheader("📋 Regulatory Context")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Basel III Requirements:**
        - **Minimum Capital Adequacy Ratio:** 8.0%
        - **Minimum Tier 1 Capital Ratio:** 6.0%
        - **Minimum Leverage Ratio:** 3.0%
        - **Capital Conservation Buffer:** 2.5%
        """)
    
    with col2:
        st.markdown("""
        **US Regulatory Standards:**
        - **Well Capitalized Banks:** CAR ≥ 10%, Tier 1 ≥ 8%, Leverage ≥ 5%
        - **Adequately Capitalized:** CAR ≥ 8%, Tier 1 ≥ 6%, Leverage ≥ 4%
        - **Stress Testing:** Required for banks >$100B assets
        """)

def render_metric_analysis(metric_data, metric_name, institution_name, metric_info):
    """Render detailed analysis for a specific capitalization metric."""
    
    # Current vs historical performance
    current_value = metric_data.iloc[-1]
    historical_avg = metric_data.mean()
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.metric(
            f"Current {metric_info['name']}",
            f"{current_value:.2f}{metric_info['unit']}",
            delta=f"{current_value - historical_avg:.2f}{metric_info['unit']} vs avg"
        )
        
        st.markdown(f"**Description:**")
        st.markdown(metric_info['description'])
        
        # Benchmark comparison
        if metric_info['benchmark']['good']:
            st.markdown(f"**Benchmarks:**")
            st.markdown(f"- Good: {metric_info['benchmark']['good']}{metric_info['unit']}")
            st.markdown(f"- Fair: {metric_info['benchmark']['fair']}{metric_info['unit']}")
            st.markdown(f"- Poor: {metric_info['benchmark']['poor']}{metric_info['unit']}")
    
    with col2:
        # Individual metric trend chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=list(range(len(metric_data))),
            y=metric_data,
            mode='lines+markers',
            name=metric_info['name'],
            line=dict(width=3),
            marker=dict(size=10)
        ))
        
        # Add benchmark lines if available
        if metric_info['benchmark']['good']:
            fig.add_hline(
                y=metric_info['benchmark']['good'],
                line_dash="dash",
                line_color="green",
                annotation_text="Good Threshold"
            )
            fig.add_hline(
                y=metric_info['benchmark']['fair'],
                line_dash="dash", 
                line_color="orange",
                annotation_text="Fair Threshold"
            )
        
        fig.update_layout(
            title=f"{metric_info['name']} Trend Analysis",
            xaxis_title="Years Ago",
            yaxis_title=f"{metric_info['name']} ({metric_info['unit']})",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # AI-generated commentary
    with st.spinner(f"Analyzing {metric_name} trends..."):
        commentary = generate_metric_commentary(
            metric_data,
            metric_name,
            institution_name,
            metric_info
        )
    
    st.markdown(f"""
    <div style="background-color: #f8f9fa; padding: 15px; border-left: 4px solid #007bff; margin: 10px 0;">
    <strong>Analysis:</strong> {commentary}
    </div>
    """, unsafe_allow_html=True)
