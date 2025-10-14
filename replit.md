# Credit Review Dashboard - Angular Application

## Overview

This is a modern financial analytics dashboard built with Angular for analyzing and reviewing the creditworthiness of major US banks and broker-dealers. The application provides comprehensive analysis across multiple financial dimensions including capitalization, asset quality, profitability, and liquidity. It features AI-powered commentary generation and an interactive chatbot using OpenAI's GPT models to provide insights on financial trends and metrics. The dashboard includes real-time data visualization, trend analysis, scoring mechanisms, and comparative benchmarking tools to support credit review decisions.

## Recent Changes

### October 2025 - Complete Angular Conversion
- **Framework Migration**: Successfully converted entire Streamlit application to Angular 20 + Node.js/Express architecture
- **Backend Conversion**: Ported all Python logic (data generation, scoring engine, commentary) to TypeScript
- **RESTful API**: Created Express backend with 7 endpoints for institutions, scores, commentary, metrics, and chat
- **Frontend Rebuild**: Angular standalone components with Signals for reactive state management
- **Signal Fix**: Resolved ngModel binding issue with institution selector using separate property
- **Chatbot Feature**: Added interactive AI-powered chatbot on Overview tab for user queries about financial data
- **Color Theme Preserved**: Hunter green (#355E3B) and cream (#FFFDD0) color palette maintained throughout Angular app

### October 2025 - SEC EDGAR Integration
- **Real Data Source**: Integrated SEC EDGAR API to fetch real 10-K and 10-Q filings for financial institutions
- **AI Analysis Pipeline**: OpenAI GPT-4o-mini analyzes SEC documents using structured 5-category prompt (Business Environment, Market Position, Risk Management, Management Quality, Regulatory Compliance)
- **Metric Extraction**: Automated extraction of key metrics (ROE, ROA, CET1, LCR, NSFR, NPL ratio, etc.) from SEC filings
- **Intelligent Caching**: 24-hour cache for EDGAR analysis results to minimize API calls and improve performance
- **Consistent Data Flow**: All endpoints (detail, scores, commentary, chat) use same EDGAR-sourced data when available
- **Graceful Fallback**: Synthetic data fallback when EDGAR or AI services unavailable
- **No Synthetic Inflation**: Missing metrics show as 0 instead of random values to maintain data integrity

### Dashboard Design
- **Navigation**: Tab-only navigation system (5 tabs: Overview, Capitalization, Asset Quality, Profitability, Liquidity)
- **Overview Tab Features**: 
  - Executive overview with category score cards
  - AI-generated executive summary
  - Interactive chatbot interface for querying financial metrics
- **Analytics Tabs**: Simplified metric displays with year-over-year changes and AI commentary
- **Responsive Design**: Mobile and tablet-friendly layout

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Angular 20 with standalone components
- **Language**: TypeScript with full type safety
- **State Management**: Angular Signals for reactive state updates
- **HTTP Communication**: Angular HttpClient for API calls
- **Layout**: Tab-based navigation with institution selector sidebar
- **Styling**: SCSS with custom hunter green/cream color theme
  - Primary: Hunter Green (#355E3B), Cream (#FFFDD0)
  - Secondary: Orange (#FF8C42), Mint (#98D8C8), Yellow (#F7B32B)
  - Design: Clean, professional financial dashboard aesthetic
- **Port Configuration**: Frontend runs on port 5000 (0.0.0.0)

### Backend Architecture
- **Runtime**: Node.js with Express framework
- **Language**: TypeScript for type safety
- **Application Structure**: Modular utility-based architecture
  - `server.ts`: Express server with API endpoints and EDGAR integration
  - `utils/edgar-service.ts`: SEC EDGAR API client for fetching 10-K/10-Q filings
  - `utils/sec-analysis-service.ts`: OpenAI-powered SEC document analysis with structured prompts
  - `utils/metrics-mapper.ts`: Maps extracted metrics to dashboard data structure
  - `utils/edgar-cache.ts`: 24-hour caching layer for EDGAR analysis results
  - `utils/ticker-mapping.ts`: Institution name to ticker/CIK mapping
  - `utils/data-generator.ts`: Synthetic financial data (fallback only)
  - `utils/scoring-engine.ts`: Credit scoring algorithm
  - `utils/commentary-generator.ts`: OpenAI integration for commentary and chatbot
- **Data Processing**: Real SEC filings + AI analysis (with synthetic fallback)
- **Scoring Engine**: Weighted scoring algorithm (Capitalization 25%, Asset Quality 30%, Profitability 25%, Liquidity 20%)
- **AI Integration**: OpenAI GPT-4o-mini for SEC analysis, commentary generation, and chatbot responses
- **Port Configuration**: Backend API runs on port 3000

### Data Layer
- **Primary Data Source**: SEC EDGAR API - Real 10-K and 10-Q filings from financial institutions
- **SEC Integration**:
  - Fetches latest 10-K (annual) and 10-Q (quarterly) filings via SEC EDGAR API
  - Extracts text from HTML/XBRL documents
  - AI analyzes using structured 5-category prompt template
  - Metrics extracted with structured METRICS SUMMARY format
  - 24-hour cache to minimize API calls
- **Fallback Data**: Synthetic data generator when EDGAR unavailable
- **Time Series**: 5-year historical data (current year from SEC + estimated previous years)
- **Metrics Coverage**: 
  - Capitalization: CAR, Tier 1 ratio, leverage ratio, RWA
  - Asset Quality: NPL ratio, loan loss provisions, coverage ratio
  - Profitability: ROA, ROE, NIM, cost-to-income, EPS
  - Liquidity: LCR, NSFR, loan-to-deposit ratio, cash ratio
- **Benchmark System**: Predefined thresholds (excellent/good/fair/poor) for each metric type
- **Storage**: In-memory caching (24-hour TTL for EDGAR data)

### Scoring and Analytics
- **Multi-dimensional Scoring**: Weighted category scoring across four dimensions
- **Scale**: 1-10 point system with categorical ratings (Excellent, Very Good, Good, Fair, Poor)
- **Methodology**: Benchmark-based evaluation with metric-specific weights within categories
- **Trend Analysis**: Year-over-year change calculations with delta indicators

### Chatbot Feature
- **Location**: Interactive chat interface on Overview tab
- **Functionality**: Users can ask questions about the selected institution's financial metrics, credit scores, and performance
- **AI Model**: OpenAI GPT-4o-mini with conversation history support
- **Context-Aware**: Chatbot has access to current institution's complete financial data, scores, and metrics
- **Fallback**: Graceful degradation to rule-based responses when OpenAI API unavailable
- **UI Design**: Styled with hunter green/cream theme, message bubbles differentiate user and assistant
- **Conversation Management**: Chat history clears when switching institutions

## External Dependencies

### Frontend Libraries
- **@angular/core**: Angular framework (v20+)
- **@angular/common**: Common Angular utilities
- **@angular/forms**: Angular forms module for two-way binding
- **rxjs**: Reactive programming with observables

### Backend Libraries
- **express**: Web application framework
- **cors**: Cross-origin resource sharing middleware
- **dotenv**: Environment variable management
- **openai**: OpenAI API client for GPT models
- **typescript**: TypeScript compiler and runtime
- **ts-node-dev**: Development server with hot reload

### APIs and Services
- **SEC EDGAR API**: Real-time access to financial institution filings
  - Base URL: `https://data.sec.gov`
  - Fetches 10-K (annual) and 10-Q (quarterly) reports
  - Rate limit: 10 requests/second (SEC requirement)
  - User-Agent: CreditDashboard/1.0 (required by SEC)
  - CIK-based lookup for accurate institution matching
  
- **OpenAI API**: AI-powered analysis and insights
  - API key configured via environment variable `OPENAI_API_KEY`
  - Model: GPT-4o-mini (cost-effective, fast responses)
  - Use cases:
    1. SEC filing analysis with 5-category structured prompt
    2. Metric extraction from documents
    3. Financial commentary generation
    4. Interactive chatbot responses
  - Fallback mechanism when API unavailable
  - Context: Full SEC analysis or synthetic data + scores passed to AI

### API Endpoints

**Institutions:**
- `GET /api/institutions` - List all financial institutions
- `GET /api/institutions/:name` - Get detailed institution data
  - **Data Flow**: Checks EdgarCache → Fetches SEC filings → AI analysis → Cache → Return
  - **Fallback**: Synthetic data if EDGAR/AI unavailable
- `GET /api/institutions/:name/scores` - Get credit scores for institution
  - **Data Source**: Uses cached EDGAR data if available, otherwise synthetic

**Commentary:**
- `POST /api/commentary` - Generate AI commentary for specific category
  - Request: `{ institutionName, category }`
  - Response: `{ commentary }`
  - **Data Source**: Uses EDGAR analysis text if cached, otherwise generates from data

**Chatbot:**
- `POST /api/chat` - Interactive chatbot conversation
  - Request: `{ institutionName, message, conversationHistory }`
  - Response: `{ message }`
  - **Context**: Uses EDGAR-sourced data when available

**Metadata:**
- `GET /api/metrics` - Get metric definitions and benchmarks
- `GET /health` - Health check endpoint
- `GET /health` - Health check endpoint

### Environment Configuration
- **Required Environment Variables**:
  - `OPENAI_API_KEY`: OpenAI API authentication key (required for AI analysis and chat)
  - `PORT`: Backend server port (defaults to 3000)
- **Optional Environment Variables**:
  - None currently (SEC EDGAR API is public and doesn't require authentication)
- **Frontend Configuration**: Angular dev server configured in `angular.json`
- **Build Configuration**: TypeScript configs for both frontend and backend
- **SEC EDGAR Compliance**: User-Agent header automatically set for SEC API compliance

## Project Structure

```
credit-review-dashboard/
├── frontend/                    # Angular application (port 5000)
│   ├── src/app/
│   │   ├── services/           # API service for backend communication
│   │   ├── app.ts              # Main dashboard component with chat
│   │   ├── app.html            # Dashboard template with chatbot UI
│   │   └── app.scss            # Hunter green/cream styling
│   └── angular.json            # Angular configuration
│
├── backend/                     # Express API server (port 3000)
│   ├── src/
│   │   ├── utils/
│   │   │   ├── data-generator.ts
│   │   │   ├── scoring-engine.ts
│   │   │   └── commentary-generator.ts
│   │   └── server.ts           # Express routes and chatbot endpoint
│   └── package.json
│
├── shared/                      # Shared TypeScript interfaces
│   └── interfaces.ts
│
├── setup-angular-dashboard.sh  # Setup script
├── start-angular-dashboard.sh  # Start both servers
└── ANGULAR-README.md           # Technical documentation
```

## Development Workflow

**Starting the Application:**
```bash
# Option 1: Using scripts
./setup-angular-dashboard.sh    # First time only
./start-angular-dashboard.sh    # Start both servers

# Option 2: Manual
# Terminal 1 - Backend
cd backend && npm run dev

# Terminal 2 - Frontend  
cd frontend && npm start
```

**Access Points:**
- Frontend Dashboard: http://localhost:5000
- Backend API: http://localhost:3000
- Health Check: http://localhost:3000/health

## Key Features

### Dashboard Tabs (5)
1. **Overview** - Executive summary, category scores, AI commentary, interactive chatbot
2. **Capitalization** - CAR, Tier 1 ratio, leverage metrics with YoY changes
3. **Asset Quality** - NPL, provisions, coverage with YoY changes
4. **Profitability** - ROA, ROE, NIM, cost-to-income with YoY changes
5. **Liquidity** - LCR, NSFR, loan-to-deposit, cash ratio with YoY changes

### Interactive Chatbot
- Ask questions about institution's financial health
- Get AI-powered explanations of metrics and scores
- Conversation history maintained per institution
- Context-aware responses based on current data
- Graceful fallback when AI unavailable

### Technical Highlights
- ✅ Full TypeScript type safety across frontend and backend
- ✅ Angular Signals for reactive state management
- ✅ RESTful API architecture for scalability
- ✅ OpenAI integration for AI-powered insights and chat
- ✅ Deterministic data generation with consistent results
- ✅ Comprehensive error handling and fallback mechanisms
- ✅ Responsive design for desktop and tablet
- ✅ Professional hunter green/cream color theme
