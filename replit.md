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
  - `server.ts`: Express server with API endpoints
  - `utils/data-generator.ts`: Synthetic financial data generation (ported from Python)
  - `utils/scoring-engine.ts`: Credit scoring algorithm (ported from Python)
  - `utils/commentary-generator.ts`: OpenAI integration for AI commentary and chatbot
- **Data Processing**: Native TypeScript/JavaScript for financial calculations
- **Scoring Engine**: Weighted scoring algorithm (Capitalization 25%, Asset Quality 30%, Profitability 25%, Liquidity 20%)
- **AI Integration**: OpenAI GPT-4o-mini for commentary generation and chatbot responses with fallback mechanism
- **Port Configuration**: Backend API runs on port 3000

### Data Layer
- **Data Generation**: Deterministic synthetic data generator creating realistic financial metrics for 10 major US institutions
- **Time Series**: 5-year historical data spanning multiple financial metrics per institution
- **Metrics Coverage**: 
  - Capitalization: CAR, Tier 1 ratio, leverage ratio, RWA
  - Asset Quality: NPL ratio, loan loss provisions, coverage ratio
  - Profitability: ROA, ROE, NIM, cost-to-income, EPS
  - Liquidity: LCR, NSFR, loan-to-deposit ratio, cash ratio
- **Benchmark System**: Predefined thresholds (excellent/good/fair/poor) for each metric type
- **Storage**: In-memory data generation (no persistent storage)

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
- **OpenAI API**: Used for generating intelligent financial commentary and chatbot responses
  - API key configured via environment variable `OPENAI_API_KEY`
  - Model: GPT-4o-mini (cost-effective, fast responses)
  - Fallback mechanism when API unavailable
  - Context: Full institution financial data and scores passed to AI

### API Endpoints

**Institutions:**
- `GET /api/institutions` - List all financial institutions
- `GET /api/institutions/:name` - Get detailed institution data
- `GET /api/institutions/:name/scores` - Get credit scores for institution

**Commentary:**
- `POST /api/commentary` - Generate AI commentary for specific category
  - Request: `{ institutionName, category }`
  - Response: `{ commentary }`

**Chatbot:**
- `POST /api/chat` - Interactive chatbot conversation
  - Request: `{ institutionName, message, conversationHistory }`
  - Response: `{ message }`

**Metadata:**
- `GET /api/metrics` - Get metric definitions and benchmarks
- `GET /health` - Health check endpoint

### Environment Configuration
- **Required Environment Variables**:
  - `OPENAI_API_KEY`: OpenAI API authentication key (optional, falls back to default commentary)
  - `PORT`: Backend server port (defaults to 3000)
- **Frontend Configuration**: Angular dev server configured in `angular.json`
- **Build Configuration**: TypeScript configs for both frontend and backend

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
