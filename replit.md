# Credit Review Dashboard

## Overview

This is a financial analytics dashboard built with Streamlit for analyzing and reviewing the creditworthiness of major US banks and broker-dealers. The application provides comprehensive analysis across multiple financial dimensions including capitalization, asset quality, profitability, and liquidity. It features AI-powered commentary generation using OpenAI's GPT models to provide insights on financial trends and metrics. The dashboard includes interactive visualizations, trend analysis, scoring mechanisms, and comparative benchmarking tools to support credit review decisions.

## Recent Changes

### October 2025 - Dashboard Redesign
- **Navigation Restructure**: Removed sidebar page navigation, implemented tab-only navigation system
- **Overview Tab Optimization**: Reorganized layout with Executive Summary moved below Executive Overview; removed Performance Radar and Key Financial Trends visualizations; removed Risk Assessment Matrix legends
- **Capitalization Tab Simplification**: Removed "Five-Year Capital Trends" and "Current Performance vs Benchmarks" sections; optimized content (reduced chart heights to 300px, compacted spacing)
- **Asset Quality Tab Simplification**: Removed "Asset Quality Trends Overview", "Current Performance vs Industry Benchmarks", and "Asset Quality Deep Dive" sections; optimized content (reduced chart heights to 300px, compacted spacing)
- **Profitability Tab Simplification**: Removed "Profitability Trends Overview", "Current Performance vs Industry Benchmarks", "Profitability Deep Dive", and "Profitability Correlation Analysis" sections; optimized content (reduced chart heights to 300px, compacted spacing)
- **Liquidity Tab Simplification**: Removed "Liquidity Trends Overview" and "Current Liquidity Position vs Regulatory Requirements" sections; optimized content (reduced chart heights to 250-300px, compacted spacing)
- **Color Theme**: Applied sophisticated hunter green (#355E3B) and cream (#FFFDD0) color palette with orange, mint, and yellow accents throughout dashboard

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit for web-based dashboard interface
- **Layout**: Tab-only navigation (no sidebar page links) with wide layout and institution selector in sidebar
- **Visualization**: Plotly (graph_objects and express) for interactive charts including trend lines, gauges, heatmaps, and bar charts
- **State Management**: Streamlit's native session state and caching mechanisms
- **Styling**: Custom CSS injected via Streamlit markdown for sophisticated themed color palette
  - Primary: Hunter Green (#355E3B), Cream (#FFFDD0)
  - Secondary: Orange (#FF8C42), Mint (#98D8C8), Yellow (#F7B32B)
  - Design: Clean, professional financial dashboard aesthetic with color-coded metrics

### Backend Architecture
- **Application Structure**: Modular view-based architecture with separate modules for each analysis category
  - `app.py`: Main entry point and tab orchestration
  - `views/`: Category-specific rendering modules (overview, capitalization, asset_quality, profitability, liquidity)
  - `utils/`: Shared utility modules for data generation, scoring, charting, and commentary
- **Data Processing**: Pandas and NumPy for financial calculations and data manipulation
- **Scoring Engine**: Custom weighted scoring algorithm across four categories with configurable benchmarks
- **AI Commentary**: OpenAI API integration with fallback mechanisms for generating financial analysis narratives

### Data Layer
- **Data Generation**: Synthetic data generator creating realistic financial metrics for 10 major US institutions
- **Time Series**: 5-year historical data spanning multiple financial metrics per institution
- **Metrics Coverage**: 
  - Capitalization: CAR, Tier 1 ratio, leverage ratio, RWA
  - Asset Quality: NPL ratio, loan loss provisions, coverage ratio
  - Profitability: ROA, ROE, NIM, cost-to-income, EPS
  - Liquidity: LCR, NSFR, loan-to-deposit ratio, cash ratio
- **Benchmark System**: Predefined thresholds (excellent/good/fair/poor) for each metric type

### Scoring and Analytics
- **Multi-dimensional Scoring**: Weighted category scoring (Capitalization 25%, Asset Quality 30%, Profitability 25%, Liquidity 20%)
- **Scale**: 1-10 point system with categorical ratings
- **Methodology**: Benchmark-based evaluation with metric-specific weights within categories
- **Trend Analysis**: Year-over-year change calculations with delta indicators

## External Dependencies

### Third-Party Libraries
- **streamlit**: Web application framework for dashboard UI
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations and array operations
- **plotly**: Interactive visualization library (both express and graph_objects modules)
- **openai**: AI-powered commentary generation (GPT-5 model as of August 2025)

### APIs and Services
- **OpenAI API**: Used for generating intelligent financial commentary and insights
  - API key configured via environment variable `OPENAI_API_KEY`
  - Model: GPT-5 (latest as of August 2025)
  - Fallback mechanism when API unavailable

### Data Storage
- **In-Memory Data**: Currently uses synthetic data generation on application load
- **No Persistent Storage**: Application does not persist data between sessions
- **Future Extensibility**: Architecture supports integration with databases (structure prepared for potential Drizzle ORM integration)

### Environment Configuration
- **Required Environment Variables**:
  - `OPENAI_API_KEY`: OpenAI API authentication key (optional, falls back to default commentary)
- **Python Dependencies**: Managed via package imports (streamlit, pandas, numpy, plotly, openai)