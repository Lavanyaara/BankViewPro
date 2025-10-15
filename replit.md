# Credit Review Dashboard - Angular Application

## Overview
This project is an Angular financial analytics dashboard designed for reviewing the creditworthiness of major US banks and broker-dealers. It provides comprehensive analysis across capitalization, asset quality, profitability, and liquidity, leveraging AI for commentary generation and an interactive chatbot. The application integrates real-time data visualization, trend analysis, scoring mechanisms, and comparative benchmarking to support credit review decisions. Its business vision is to provide a modern, AI-augmented tool for financial analysts, enhancing efficiency and depth of credit assessment in the financial sector.

## User Preferences
Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend
- **Framework**: Angular 20 with standalone components and Signals for reactive state management.
- **Styling**: SCSS with a custom hunter green (#355E3B) and cream (#FFFDD0) color theme, aiming for a clean, professional financial dashboard aesthetic.
- **Layout**: Tab-based navigation system (Overview, Capitalization, Asset Quality, Profitability, Liquidity) with an institution selector sidebar.
- **Key Features**:
    - **Flow Type Selector**: Dropdown to select between "Bank Flow" and "Broker Flow"
      - Bank Flow: Shows 9 banks, uses SEC EDGAR + FFIEC Call Reports for data
      - Broker Flow: Shows 6 broker-dealers, uses FINRA BrokerCheck + SEC EDGAR for data
    - **Calculation Logic Toggle**: Independent checkbox to switch between bank and broker-dealer calculation formulas (different thresholds and weights)
    - **Overview Tab**: Executive summary, category score cards, AI-generated summary, and an interactive AI chatbot.
    - **Analytics Tabs**: Simplified metric displays with year-over-year changes and AI commentary.
    - **Responsiveness**: Designed for mobile and tablet compatibility.

### Backend
- **Runtime**: Node.js with Express framework, written in TypeScript.
- **Architecture**: Modular, utility-based structure with smart routing to handle different institution types.
- **Data Processing**: Integrates multi-source regulatory data (SEC EDGAR, FINRA BrokerCheck, FFIEC Call Reports) with AI analysis. Includes a 24-hour caching mechanism for analyzed data and falls back to synthetic data if regulatory sources or AI services are unavailable.
- **Scoring Engine**: Implements a weighted algorithm for multi-dimensional credit scoring (1-10 scale with categorical ratings).
- **AI Integration**: Utilizes OpenAI's GPT-4o-mini for:
    - Multi-source document analysis (SEC filings, FINRA, FFIEC).
    - Extraction of key financial metrics.
    - Generation of financial commentary.
    - Powering the interactive chatbot with context-aware responses.
- **API Endpoints**: Provides RESTful endpoints for institutions, scores, commentary, and chat.

### Data Layer
- **Multi-Source**: Dynamically fetches data based on institution type:
    - **Banks**: SEC EDGAR (10-K/10-Q) + FFIEC Call Reports.
    - **Broker-Dealers**: FINRA BrokerCheck + SEC EDGAR (when available).
- **AI Analysis Pipeline**: OpenAI GPT-4o-mini processes documents using a structured 5-category prompt, extracting key financial metrics.
- **Historical Data**: Provides 5-year historical data (current year from regulatory sources + estimated previous years).
- **Benchmarking**: Includes predefined thresholds for metric evaluation (excellent/good/fair/poor).

### Chatbot
- **Location**: Integrated into the Overview tab.
- **Functionality**: Allows users to query financial metrics, credit scores, and performance, with context-aware responses and conversation history per institution.

## External Dependencies

### Frontend Libraries
- **@angular/core**: Core Angular framework.
- **@angular/forms**: For two-way data binding.
- **rxjs**: For reactive programming.

### Backend Libraries
- **express**: Web application framework.
- **cors**: Middleware for Cross-Origin Resource Sharing.
- **dotenv**: Environment variable management.
- **openai**: OpenAI API client.
- **typescript**: For TypeScript compilation.

### APIs and Services
- **SEC EDGAR API**: For fetching 10-K and 10-Q filings.
- **FINRA BrokerCheck**: Provides regulatory data for broker-dealers (structured text generation due to lack of public API).
- **FFIEC Call Reports**: Provides detailed bank regulatory filings (structured text generation due to authentication requirements for full API access).
- **OpenAI API**: Uses GPT-4o-mini for AI analysis, commentary generation, and chatbot functionality. Authenticated via `OPENAI_API_KEY`.