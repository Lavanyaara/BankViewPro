import streamlit as st
import plotly.graph_objects as go
import numpy as np
from utils.chart_generator import create_trend_chart, create_metric_gauge, create_correlation_heatmap
from utils.commentary_generator import generate_metric_commentary, generate_section_commentary
from utils.data_generator import get_metric_info

def render_asset_quality(bank_data, institution_name):
    """Render the Asset Quality tab with NPL, provisions, and coverage metrics."""
    
    st.header("📈 Asset Quality Analysis")
    
    # Get historical data
    historical_data = bank_data['historical_data']
    latest_data = historical_data.iloc[-1]
    
    # Get metric information
    metric_info = get_metric_info()['asset_quality']
    
    # Key asset quality metrics
    asset_metrics = [
        'npl_ratio',
        'loan_loss_provisions',
        'coverage_ratio',
        'asset_classification'
    ]
    
    # Display current metrics
    st.subheader("Current Asset Quality Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        prev_npl = historical_data.iloc[-2]['npl_ratio']
        delta_npl = latest_data['npl_ratio'] - prev_npl
        st.metric(
            "NPL Ratio",
            f"{latest_data['npl_ratio']:.2f}%",
            delta=f"{delta_npl:.2f}%",
            delta_color="inverse"  # Lower NPL is better
        )
    
    with col2:
        prev_provisions = historical_data.iloc[-2]['loan_loss_provisions']
        delta_provisions = latest_data['loan_loss_provisions'] - prev_provisions
        st.metric(
            "Loan Loss Provisions",
            f"{latest_data['loan_loss_provisions']:.2f}%",
            delta=f"{delta_provisions:.2f}%",
            delta_color="inverse"  # Lower provisions are better
        )
    
    with col3:
        prev_coverage = historical_data.iloc[-2]['coverage_ratio']
        delta_coverage = latest_data['coverage_ratio'] - prev_coverage
        st.metric(
            "Coverage Ratio",
            f"{latest_data['coverage_ratio']:.1f}%",
            delta=f"{delta_coverage:.1f}%"
        )
    
    with col4:
        prev_classification = historical_data.iloc[-2]['asset_classification']
        delta_classification = latest_data['asset_classification'] - prev_classification
        st.metric(
            "Asset Classification",
            f"{latest_data['asset_classification']:.1f}",
            delta=f"{delta_classification:.1f}",
            delta_color="inverse"  # Lower classification score is better
        )
    
    st.divider()
    
    # Asset Quality Overview Chart
    st.subheader("📊 Asset Quality Trends Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # NPL and Provisions trend (inverted scale since lower is better)
        fig_quality = go.Figure()
        
        fig_quality.add_trace(go.Scatter(
            x=historical_data['year'],
            y=historical_data['npl_ratio'],
            mode='lines+markers',
            name='NPL Ratio',
            line=dict(color='#d62728', width=3),
            marker=dict(size=8),
            yaxis='y'
        ))
        
        fig_quality.add_trace(go.Scatter(
            x=historical_data['year'],
            y=historical_data['loan_loss_provisions'],
            mode='lines+markers',
            name='Loan Loss Provisions',
            line=dict(color='#ff7f0e', width=3),
            marker=dict(size=8),
            yaxis='y'
        ))
        
        fig_quality.update_layout(
            title="Problem Assets Trend (Lower is Better)",
            xaxis_title="Year",
            yaxis_title="Percentage (%)",
            height=400,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_quality, use_container_width=True)
    
    with col2:
        # Coverage and Classification
        fig_coverage = go.Figure()
        
        fig_coverage.add_trace(go.Scatter(
            x=historical_data['year'],
            y=historical_data['coverage_ratio'],
            mode='lines+markers',
            name='Coverage Ratio',
            line=dict(color='#2ca02c', width=3),
            marker=dict(size=8),
            yaxis='y'
        ))
        
        # Add secondary y-axis for asset classification
        fig_coverage.add_trace(go.Scatter(
            x=historical_data['year'],
            y=historical_data['asset_classification'],
            mode='lines+markers',
            name='Asset Classification Score',
            line=dict(color='#9467bd', width=3),
            marker=dict(size=8),
            yaxis='y2'
        ))
        
        fig_coverage.update_layout(
            title="Coverage & Classification Trends",
            xaxis_title="Year",
            yaxis=dict(title="Coverage Ratio (%)", side='left'),
            yaxis2=dict(title="Classification Score", side='right', overlaying='y'),
            height=400,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_coverage, use_container_width=True)
    
    st.divider()
    
    # Performance Gauges
    st.subheader("🎯 Current Performance vs Industry Benchmarks")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # NPL Ratio Gauge (lower is better)
        npl_info = metric_info['npl_ratio']
        fig_npl_gauge = create_metric_gauge(
            latest_data['npl_ratio'],
            npl_info['benchmark']['good'],
            npl_info['benchmark']['fair'],
            "NPL Ratio",
            "%"
        )
        st.plotly_chart(fig_npl_gauge, use_container_width=True)
    
    with col2:
        # Coverage Ratio Gauge (higher is better)
        coverage_info = metric_info['coverage_ratio']
        fig_coverage_gauge = create_metric_gauge(
            latest_data['coverage_ratio'],
            coverage_info['benchmark']['good'],
            coverage_info['benchmark']['fair'],
            "Coverage Ratio",
            "%"
        )
        st.plotly_chart(fig_coverage_gauge, use_container_width=True)
    
    with col3:
        # Provisions Gauge (lower is better)
        provisions_info = metric_info['loan_loss_provisions']
        fig_provisions_gauge = create_metric_gauge(
            latest_data['loan_loss_provisions'],
            provisions_info['benchmark']['good'],
            provisions_info['benchmark']['fair'],
            "Loan Loss Provisions",
            "%"
        )
        st.plotly_chart(fig_provisions_gauge, use_container_width=True)
    
    st.divider()
    
    # Asset Quality Deep Dive
    st.subheader("🔍 Asset Quality Deep Dive")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Asset quality correlation heatmap
        correlation_metrics = ['npl_ratio', 'loan_loss_provisions', 'coverage_ratio', 'asset_classification']
        fig_corr = create_correlation_heatmap(
            historical_data,
            correlation_metrics,
            "Asset Quality Metrics Correlation"
        )
        st.plotly_chart(fig_corr, use_container_width=True)
    
    with col2:
        # Asset quality risk assessment
        st.markdown("#### Risk Assessment")
        
        # Calculate risk indicators
        npl_trend = latest_data['npl_ratio'] - historical_data['npl_ratio'].iloc[0]
        coverage_adequacy = latest_data['coverage_ratio']
        provisions_trend = latest_data['loan_loss_provisions'] - historical_data['loan_loss_provisions'].iloc[0]
        
        risk_score = calculate_asset_quality_risk_score(latest_data)
        
        st.metric("Asset Quality Risk Score", f"{risk_score:.1f}/10", 
                 help="Higher scores indicate higher risk")
        
        # Risk factors
        st.markdown("**Key Risk Factors:**")
        
        if npl_trend > 0.5:
            st.markdown("🔴 Rising NPL trend")
        elif npl_trend < -0.2:
            st.markdown("🟢 Improving NPL trend")
        else:
            st.markdown("🟡 Stable NPL levels")
        
        if coverage_adequacy < 80:
            st.markdown("🔴 Low coverage ratio")
        elif coverage_adequacy > 100:
            st.markdown("🟢 Strong coverage ratio")
        else:
            st.markdown("🟡 Adequate coverage")
        
        if provisions_trend > 0.3:
            st.markdown("🔴 Rising provisions")
        elif provisions_trend < -0.1:
            st.markdown("🟢 Declining provisions")
        else:
            st.markdown("🟡 Stable provisions")
    
    st.divider()
    
    # Detailed Metric Analysis Tabs
    st.subheader("📋 Detailed Metric Analysis")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "NPL Ratio",
        "Loan Loss Provisions",
        "Coverage Ratio", 
        "Asset Classification"
    ])
    
    with tab1:
        render_asset_metric_analysis(
            historical_data['npl_ratio'],
            'npl_ratio',
            institution_name,
            metric_info['npl_ratio']
        )
    
    with tab2:
        render_asset_metric_analysis(
            historical_data['loan_loss_provisions'],
            'loan_loss_provisions',
            institution_name,
            metric_info['loan_loss_provisions']
        )
    
    with tab3:
        render_asset_metric_analysis(
            historical_data['coverage_ratio'],
            'coverage_ratio',
            institution_name,
            metric_info['coverage_ratio']
        )
    
    with tab4:
        render_asset_metric_analysis(
            historical_data['asset_classification'],
            'asset_classification',
            institution_name,
            metric_info['asset_classification']
        )
    
    st.divider()
    
    # Overall Asset Quality Commentary
    st.subheader("💬 Asset Quality Assessment Summary")
    
    section_data = {
        'npl_ratio': historical_data['npl_ratio'],
        'loan_loss_provisions': historical_data['loan_loss_provisions'],
        'coverage_ratio': historical_data['coverage_ratio'],
        'asset_classification': historical_data['asset_classification']
    }
    
    with st.spinner("Generating asset quality analysis..."):
        section_commentary = generate_section_commentary(
            section_data,
            "Asset Quality",
            institution_name
        )
    
    st.markdown(f"""
    <div style="background-color: #fff3cd; padding: 20px; border-radius: 10px; margin: 10px 0;">
    <h4>Asset Quality Summary</h4>
    <p style="font-size: 16px; line-height: 1.6;">{section_commentary}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Industry Context
    st.subheader("🏭 Industry Context & Benchmarks")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Industry Benchmarks (US Banks):**
        - **Excellent NPL Ratio:** < 1.0%
        - **Good NPL Ratio:** 1.0% - 2.0%  
        - **Poor NPL Ratio:** > 3.0%
        - **Typical Coverage Ratio:** 80% - 120%
        """)
    
    with col2:
        st.markdown("""
        **Regulatory Guidelines:**
        - **ALLL Adequacy:** Must cover expected losses
        - **Stress Testing:** Required for large institutions
        - **Early Warning Indicators:** NPL > 4%, Coverage < 60%
        - **Asset Classification:** 1=Pass, 5=Loss
        """)

def render_asset_metric_analysis(metric_data, metric_name, institution_name, metric_info):
    """Render detailed analysis for a specific asset quality metric."""
    
    current_value = metric_data.iloc[-1]
    historical_avg = metric_data.mean()
    volatility = metric_data.std()
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.metric(
            f"Current {metric_info['name']}",
            f"{current_value:.2f}{metric_info['unit']}",
            delta=f"{current_value - historical_avg:.2f}{metric_info['unit']} vs avg"
        )
        
        st.markdown(f"**Volatility:** {volatility:.2f}{metric_info['unit']}")
        st.markdown(f"**Description:** {metric_info['description']}")
        
        # Performance assessment
        benchmark = metric_info['benchmark']
        if benchmark['good'] is not None:
            if 'npl' in metric_name.lower() or 'provisions' in metric_name.lower() or 'classification' in metric_name.lower():
                # Lower is better for these metrics
                if current_value <= benchmark['good']:
                    performance = "🟢 Excellent"
                elif current_value <= benchmark['fair']:
                    performance = "🟡 Good" 
                elif current_value <= benchmark['poor']:
                    performance = "🟠 Fair"
                else:
                    performance = "🔴 Poor"
            else:
                # Higher is better for coverage ratio
                if current_value >= benchmark['good']:
                    performance = "🟢 Excellent"
                elif current_value >= benchmark['fair']:
                    performance = "🟡 Good"
                elif current_value >= benchmark['poor']:
                    performance = "🟠 Fair"
                else:
                    performance = "🔴 Poor"
            
            st.markdown(f"**Performance:** {performance}")
    
    with col2:
        # Trend chart with benchmark lines
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
        
        # Add benchmark lines
        if metric_info['benchmark']['good'] is not None:
            fig.add_hline(
                y=metric_info['benchmark']['good'],
                line_dash="dash",
                line_color="green",
                annotation_text="Good Threshold",
                annotation_position="top right"
            )
            fig.add_hline(
                y=metric_info['benchmark']['fair'],
                line_dash="dash",
                line_color="orange", 
                annotation_text="Fair Threshold",
                annotation_position="bottom right"
            )
            fig.add_hline(
                y=metric_info['benchmark']['poor'],
                line_dash="dash",
                line_color="red",
                annotation_text="Poor Threshold",
                annotation_position="bottom right"
            )
        
        fig.update_layout(
            title=f"{metric_info['name']} Historical Trend",
            xaxis_title="Year",
            yaxis_title=f"{metric_info['name']} ({metric_info['unit']})",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # AI Commentary
    with st.spinner(f"Analyzing {metric_name} performance..."):
        commentary = generate_metric_commentary(
            metric_data,
            metric_name,
            institution_name,
            metric_info
        )
    
    st.markdown(f"""
    <div style="background-color: #f8f9fa; padding: 15px; border-left: 4px solid #28a745; margin: 10px 0;">
    <strong>Analysis:</strong> {commentary}
    </div>
    """, unsafe_allow_html=True)

def calculate_asset_quality_risk_score(latest_data):
    """Calculate asset quality risk score (1-10, higher = more risk)."""
    
    risk_score = 5.0  # Base neutral score
    
    # NPL Ratio impact
    npl = latest_data['npl_ratio']
    if npl > 3.0:
        risk_score += 2.0
    elif npl > 2.0:
        risk_score += 1.0
    elif npl < 1.0:
        risk_score -= 1.0
    
    # Coverage Ratio impact
    coverage = latest_data['coverage_ratio']
    if coverage < 60:
        risk_score += 1.5
    elif coverage > 100:
        risk_score -= 0.5
    
    # Loan Loss Provisions impact
    provisions = latest_data['loan_loss_provisions']
    if provisions > 1.5:
        risk_score += 1.0
    elif provisions < 0.5:
        risk_score -= 0.5
    
    # Asset Classification impact
    classification = latest_data['asset_classification']
    if classification > 5:
        risk_score += 1.0
    elif classification < 3:
        risk_score -= 0.5
    
    return min(10.0, max(1.0, risk_score))
