import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# Import page modules
from pages.overview import render_overview
from pages.capitalization import render_capitalization
from pages.asset_quality import render_asset_quality
from pages.profitability import render_profitability
from pages.liquidity import render_liquidity

# Import utilities
from utils.data_generator import generate_sample_data
from utils.scoring_engine import calculate_overall_score

def main():
    st.set_page_config(
        page_title="Credit Review Dashboard",
        page_icon="🏦",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🏦 Credit Review Dashboard")
    st.subheader("Comprehensive Analytics for US Banks and Broker Dealers")
    
    # Initialize session state for data
    if 'bank_data' not in st.session_state:
        st.session_state.bank_data = generate_sample_data()
    
    # Sidebar for bank selection
    st.sidebar.header("Institution Selection")
    available_banks = list(st.session_state.bank_data.keys())
    selected_bank = st.sidebar.selectbox(
        "Select Financial Institution:",
        available_banks,
        index=0
    )
    
    # Store selected bank in session state
    st.session_state.selected_bank = selected_bank
    
    # Display selected bank info
    st.sidebar.markdown(f"**Selected:** {selected_bank}")
    
    # Calculate and display overall score
    overall_score = calculate_overall_score(st.session_state.bank_data[selected_bank])
    st.sidebar.metric(
        "Overall Credit Score", 
        f"{overall_score:.1f}/10.0",
        delta=None
    )
    
    # Score interpretation
    if overall_score >= 8.0:
        score_status = "🟢 Excellent"
    elif overall_score >= 6.5:
        score_status = "🟡 Good"
    elif overall_score >= 5.0:
        score_status = "🟠 Fair"
    else:
        score_status = "🔴 Poor"
    
    st.sidebar.markdown(f"**Rating:** {score_status}")
    
    # Tab navigation
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview",
        "💰 Capitalization", 
        "📈 Asset Quality",
        "💵 Profitability",
        "💧 Liquidity"
    ])
    
    with tab1:
        render_overview(st.session_state.bank_data[selected_bank], selected_bank)
    
    with tab2:
        render_capitalization(st.session_state.bank_data[selected_bank], selected_bank)
    
    with tab3:
        render_asset_quality(st.session_state.bank_data[selected_bank], selected_bank)
    
    with tab4:
        render_profitability(st.session_state.bank_data[selected_bank], selected_bank)
    
    with tab5:
        render_liquidity(st.session_state.bank_data[selected_bank], selected_bank)

if __name__ == "__main__":
    main()
