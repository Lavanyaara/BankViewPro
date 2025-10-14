# Credit Review Dashboard - Angular Application

## Overview

This is an Angular-based credit review dashboard for analyzing US Banks and Broker Dealers. The application features comprehensive financial analytics across multiple dimensions including capitalization, asset quality, profitability, and liquidity with AI-powered commentary using OpenAI GPT.

## Architecture

### Frontend (Angular 20+)
- **Framework**: Angular with standalone components
- **Styling**: SCSS with hunter green (#355E3B) and cream (#FFFDD0) color theme
- **HTTP Client**: Angular HttpClient for API communication
- **State Management**: Angular Signals for reactive state
- **Tab Navigation**: Custom tab-based interface (no sidebar page links)

### Backend (Node.js/Express + TypeScript)
- **Runtime**: Node.js with Express server
- **Language**: TypeScript for type safety
- **Data Layer**: Synthetic data generation with deterministic seeding
- **Scoring Engine**: Weighted category scoring algorithm
- **AI Integration**: OpenAI API for commentary generation with fallback

### Shared
- **TypeScript Interfaces**: Shared types between frontend and backend
- **Consistent Data Models**: Institution, HistoricalRecord, CategoryScores

## Project Structure

```
.
├── frontend/                 # Angular application
│   ├── src/
│   │   ├── app/
│   │   │   ├── services/    # API service for backend communication
│   │   │   ├── app.ts       # Main dashboard component
│   │   │   ├── app.html     # Dashboard template
│   │   │   ├── app.scss     # Styling with color theme
│   │   │   └── app.config.ts
│   │   ├── index.html
│   │   └── main.ts
│   ├── angular.json
│   ├── package.json
│   └── tsconfig.json
│
├── backend/                  # Express API server
│   ├── src/
│   │   ├── utils/
│   │   │   ├── data-generator.ts     # Synthetic data generation
│   │   │   ├── scoring-engine.ts     # Credit scoring logic
│   │   │   └── commentary-generator.ts # OpenAI integration
│   │   └── server.ts         # Express server setup
│   ├── package.json
│   ├── tsconfig.json
│   └── .env                  # Environment variables
│
└── shared/                   # Shared TypeScript interfaces
    └── interfaces.ts
```

## Setup Instructions

### Prerequisites
- Node.js 20+ installed
- npm package manager
- OpenAI API key (optional, for AI commentary)

### Installation Steps

1. **Install Backend Dependencies**
   ```bash
   cd backend
   npm install
   ```

2. **Install Frontend Dependencies**
   ```bash
   cd frontend
   npm install
   ```

3. **Configure Environment Variables**
   
   Create `backend/.env` file:
   ```env
   PORT=3000
   OPENAI_API_KEY=your_openai_api_key_here
   ```
   
   *Note: If no OpenAI API key is provided, the application will use default fallback commentary.*

4. **Start Backend Server**
   ```bash
   cd backend
   npm run dev
   ```
   
   The backend API will start on `http://localhost:3000`

5. **Start Frontend Application**
   ```bash
   cd frontend
   npm start
   ```
   
   The Angular app will start on `http://localhost:4200`

## Features

### Dashboard Tabs
1. **Overview**: Executive summary with category scores and AI commentary
2. **Capitalization**: Capital adequacy, Tier 1 ratio, leverage analysis
3. **Asset Quality**: NPL ratio, loan loss provisions, coverage metrics
4. **Profitability**: ROA, ROE, NIM, cost-to-income analysis
5. **Liquidity**: LCR, NSFR, loan-to-deposit, cash ratio metrics

### Key Functionality
- **Institution Selector**: Choose from 10 major US financial institutions
- **Real-time Scoring**: Multi-dimensional credit scoring (1-10 scale)
- **Trend Analysis**: Year-over-year change calculations
- **AI Commentary**: OpenAI-powered insights for each category
- **Responsive Design**: Works on desktop and tablet devices

## API Endpoints

### GET /api/institutions
Returns list of all financial institutions

### GET /api/institutions/:name
Returns detailed data for a specific institution

### GET /api/institutions/:name/scores
Returns category scores for an institution

### POST /api/commentary
Request body: `{ institutionName: string, category: string }`
Returns AI-generated commentary

### GET /api/metrics
Returns metric information and benchmarks

### GET /health
Health check endpoint

## Color Theme

The dashboard uses a sophisticated color palette:
- **Primary**: Hunter Green (#355E3B), Cream (#FFFDD0)
- **Secondary**: Orange (#FF8C42), Mint (#98D8C8), Yellow (#F7B32B)
- **Accents**: Color-coded score indicators

## Technology Stack

### Frontend
- Angular 20+
- TypeScript
- SCSS
- HttpClient
- Signals (reactive state)

### Backend
- Node.js
- Express
- TypeScript
- OpenAI API
- ts-node-dev (development)

### Data
- Synthetic financial data (10 institutions, 5-year history)
- Deterministic random generation for consistency
- Weighted scoring algorithm

## Development

### Backend Development
```bash
cd backend
npm run dev    # Start with hot reload
npm run build  # Build for production
npm start      # Run production build
```

### Frontend Development
```bash
cd frontend
npm start      # Start development server
npm run build  # Build for production
```

## Deployment

### Backend
1. Build: `cd backend && npm run build`
2. Set environment variables (PORT, OPENAI_API_KEY)
3. Run: `node dist/server.js`

### Frontend
1. Build: `cd frontend && npm run build`
2. Serve the `dist/` folder with a static file server
3. Configure API URL in environment files

## Scoring Methodology

### Category Weights
- Capitalization: 25%
- Asset Quality: 30%
- Profitability: 25%
- Liquidity: 20%

### Score Scale
- 8.5-10.0: Excellent
- 7.0-8.4: Very Good
- 5.5-6.9: Good
- 4.0-5.4: Fair
- 1.0-3.9: Poor

## Credits

Converted from Streamlit-based dashboard to Angular application.
Original features preserved with enhanced architecture and TypeScript type safety.
