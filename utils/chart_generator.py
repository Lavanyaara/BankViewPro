import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

def create_trend_chart(data, metrics, title, y_axis_title, colors=None):
    """
    Create an interactive trend chart for multiple metrics over time.
    
    Args:
        data: DataFrame with yearly data
        metrics: List of metric column names to plot
        title: Chart title
        y_axis_title: Y-axis title
        colors: Optional list of colors for each metric
    """
    fig = go.Figure()
    
    if colors is None:
        colors = px.colors.qualitative.Set1
    
    for i, metric in enumerate(metrics):
        fig.add_trace(
            go.Scatter(
                x=data['year'],
                y=data[metric],
                mode='lines+markers',
                name=metric.replace('_', ' ').title(),
                line=dict(color=colors[i % len(colors)], width=3),
                marker=dict(size=8),
                hovertemplate=f'<b>{metric.replace("_", " ").title()}</b><br>' +
                             'Year: %{x}<br>' +
                             'Value: %{y:.2f}<br>' +
                             '<extra></extra>'
            )
        )
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=20)),
        xaxis_title="Year",
        yaxis_title=y_axis_title,
        hovermode='x unified',
        showlegend=True,
        height=500,
        margin=dict(l=0, r=0, t=50, b=0)
    )
    
    return fig

def create_metric_gauge(current_value, benchmark_good, benchmark_fair, metric_name, unit=""):
    """
    Create a gauge chart showing current metric value against benchmarks.
    
    Args:
        current_value: Current metric value
        benchmark_good: Good performance threshold
        benchmark_fair: Fair performance threshold  
        metric_name: Name of the metric
        unit: Unit of measurement
    """
    
    # Determine color based on performance
    if benchmark_good > benchmark_fair:  # Higher is better
        if current_value >= benchmark_good:
            color = "green"
        elif current_value >= benchmark_fair:
            color = "yellow"
        else:
            color = "red"
        max_range = max(current_value * 1.2, benchmark_good * 1.2)
    else:  # Lower is better
        if current_value <= benchmark_good:
            color = "green"
        elif current_value <= benchmark_fair:
            color = "yellow"
        else:
            color = "red"
        max_range = max(current_value * 1.5, benchmark_fair * 1.5)
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=current_value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"{metric_name} ({unit})"},
        gauge={
            'axis': {'range': [None, max_range]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, benchmark_good if benchmark_good < benchmark_fair else benchmark_fair], 'color': "lightgray"},
                {'range': [benchmark_good if benchmark_good < benchmark_fair else benchmark_fair, 
                          benchmark_fair if benchmark_good < benchmark_fair else benchmark_good], 'color': "gray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': current_value
            }
        }
    ))
    
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=60, b=20))
    return fig

def create_comparison_bar_chart(data, metric, institutions, title):
    """
    Create a bar chart comparing a metric across institutions.
    
    Args:
        data: Dictionary of bank data
        metric: Metric to compare
        institutions: List of institution names
        title: Chart title
    """
    values = []
    names = []
    
    for institution in institutions:
        if institution in data:
            latest_value = data[institution]['historical_data'][metric].iloc[-1]
            values.append(latest_value)
            names.append(institution.split()[0])  # Use first word for brevity
    
    fig = go.Figure(data=[
        go.Bar(
            x=names,
            y=values,
            marker_color=px.colors.qualitative.Set1[0]
        )
    ])
    
    fig.update_layout(
        title=title,
        xaxis_title="Institution",
        yaxis_title=metric.replace('_', ' ').title(),
        height=400
    )
    
    return fig

def create_correlation_heatmap(data, metrics, title):
    """
    Create a correlation heatmap for selected metrics.
    
    Args:
        data: DataFrame with metrics data
        metrics: List of metrics to include in correlation
        title: Chart title
    """
    corr_matrix = data[metrics].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=[m.replace('_', ' ').title() for m in corr_matrix.columns],
        y=[m.replace('_', ' ').title() for m in corr_matrix.index],
        colorscale='RdBu',
        zmid=0,
        text=np.round(corr_matrix.values, 2),
        texttemplate="%{text}",
        textfont={"size": 10},
        hoverongaps=False
    ))
    
    fig.update_layout(
        title=title,
        height=500,
        margin=dict(l=0, r=0, t=50, b=0)
    )
    
    return fig

def create_performance_radar(current_data, benchmarks, metrics, institution_name):
    """
    Create a radar chart showing performance across multiple dimensions.
    
    Args:
        current_data: Current year data for the institution
        benchmarks: Dictionary of benchmark values
        metrics: List of metrics to include
        institution_name: Name of the institution
    """
    
    # Normalize values to 0-100 scale based on benchmarks
    normalized_values = []
    metric_names = []
    
    for metric in metrics:
        if metric in benchmarks and metric in current_data:
            current_val = current_data[metric]
            benchmark_info = benchmarks[metric]
            
            # Extract benchmark values
            if 'benchmark' in benchmark_info:
                benchmark = benchmark_info['benchmark']
            else:
                continue
            
            # Skip if benchmark values are None
            if benchmark.get('good') is None or benchmark.get('fair') is None:
                continue
            
            if benchmark['good'] > benchmark['fair']:  # Higher is better
                if current_val >= benchmark['good']:
                    normalized = 100
                elif current_val >= benchmark['fair']:
                    normalized = 50 + 50 * (current_val - benchmark['fair']) / (benchmark['good'] - benchmark['fair'])
                else:
                    normalized = 50 * current_val / benchmark['fair'] if benchmark['fair'] > 0 else 0
            else:  # Lower is better
                if current_val <= benchmark['good']:
                    normalized = 100
                elif current_val <= benchmark['fair']:
                    normalized = 50 + 50 * (benchmark['fair'] - current_val) / (benchmark['fair'] - benchmark['good'])
                else:
                    normalized = 50 * benchmark['fair'] / current_val if current_val > 0 else 0
            
            normalized_values.append(max(0, min(100, normalized)))
            metric_names.append(metric.replace('_', ' ').title())
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=normalized_values + [normalized_values[0]],  # Close the polygon
        theta=metric_names + [metric_names[0]],
        fill='toself',
        name=institution_name,
        line=dict(color='rgb(32, 146, 230)', width=2),
        fillcolor='rgba(32, 146, 230, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title=f"Performance Radar - {institution_name}",
        height=500
    )
    
    return fig
