# Portfolio Collinearity Analyzer

**AI Dev Tools Zoomcamp - Final Project**

A full-stack application that detects redundant assets in financial portfolios by analyzing historical price correlations and coefficients of determination (R²). This project demonstrates end-to-end AI-assisted development, from architecture design to production deployment.

---

## Table of Contents
- [Project Overview](#project-overview)
- [System Functionality](#system-functionality)
- [AI-Assisted Development](#ai-assisted-development)
- [Technologies & Architecture](#technologies--architecture)
- [Frontend](#frontend)
- [API Contract (OpenAPI)](#api-contract-openapi)
- [Backend](#backend)
- [Data & Persistence](#data--persistence)
- [Containerization](#containerization)
- [Integration Testing](#integration-testing)
- [CI/CD Pipeline](#cicd-pipeline)
- [Deployment](#deployment)
- [Reproducibility](#reproducibility)
- [Project Status & Limitations](#project-status--limitations)

---

## Project Overview

### Problem Statement

In portfolio management, **collinearity** (high correlation between assets) reduces diversification benefits and concentrates risk. When assets are highly correlated, they tend to move together, meaning portfolio losses occur simultaneously rather than being offset by uncorrelated holdings.

This application addresses the problem by:
1. Fetching historical price data for user-specified assets
2. Computing pairwise Pearson correlations and R² values
3. Identifying asset pairs with R² > 0.5 (indicating >50% shared variance)
4. Presenting results through an interactive web interface

**Why This Matters:**
- **Risk Management**: Identifies hidden concentration risk in seemingly diversified portfolios
- **Capital Efficiency**: Helps reallocate capital from redundant to truly diversifying assets
- **Investment Decision Support**: Provides quantitative evidence for portfolio rebalancing

### Expected Output

Given a list of tickers (e.g., `AAPL, MSFT, GOOG, TSLA`) and an investment horizon (e.g., 1 year), the system returns:
- **Correlation Matrix**: Full pairwise correlation table
- **High R² Pairs**: List of asset pairs with R² > 0.5, sorted by strength

---

## System Functionality

### End-to-End Workflow

1. **User Input** (Frontend)
   - User enters comma-separated tickers via web form
   - Selects investment horizon (1-10 years)
   - Submits analysis request

2. **Data Fetching** (Backend)
   - Backend receives POST request at `/analyze` endpoint
   - Fetches historical daily prices from Yahoo Finance API (`yfinance`)
   - Handles missing data and aligns time series to common date index
   - Falls back to mock random walk data if API fails

3. **Statistical Analysis** (Backend)
   - Computes daily returns from price series
   - Calculates Pearson correlation matrix
   - Computes R² matrix (correlation²)
   - Identifies pairs where R² > 0.5

4. **Results Presentation** (Frontend)
   - Displays correlation matrix as interactive HTML table
   - Lists high-collinearity pairs with correlation and R² values
   - Provides visual feedback on data quality

### User Interaction

The frontend is a single-page React application with:
- **Input Form**: Text area for tickers, number input for horizon
- **Loading State**: Visual feedback during API call
- **Results Display**: Tabular correlation matrix + list of flagged pairs
- **Error Handling**: User-friendly messages for validation errors or API failures

---

## AI-Assisted Development

This project was developed using AI tools throughout the entire software development lifecycle, demonstrating practical application of AI-assisted engineering workflows.

### Tools Used

**1. ChatGPT (OpenAI)**
- **Architecture Design**: Discussed system requirements, debated FastAPI vs Flask, decided on React for frontend
- **Requirements Clarification**: Refined the definition of "collinearity" in financial context, determined appropriate R² threshold
- **Prompt Engineering**: Crafted detailed prompts for Antigravity to generate specific components
- **Problem Solving**: Debugged timezone-aware pandas index issues, SQLite locking in Docker containers

**2. Antigravity (Agentic Coding Assistant)**
- **Code Generation**: Generated complete backend (FastAPI app, data fetching, analysis logic, Pydantic models)
- **Frontend Development**: Created React components, form handling, API integration, CSS styling
- **Testing Infrastructure**: Implemented pytest suite for backend, fixed React default tests
- **CI/CD Pipeline**: Built GitHub Actions workflow with unit tests, integration tests, and deployment automation
- **Containerization**: Created multi-stage Dockerfile for unified deployment
- **Refactoring**: Migrated dependency management from pip to `uv`, updated all documentation

### Development Workflow

**Iterative Prompt Refinement:**
1. Initial prompt: "Create a FastAPI backend for portfolio analysis"
2. Refined: "Create a FastAPI backend with `/analyze` endpoint that accepts ISINs, fetches data from yfinance, computes correlation matrix, and returns JSON"
3. Further refined: "Handle timezone-aware pandas indices, implement fallback to mock data, add input validation with Pydantic min_items=2"

**AI Assistance Acceleration:**
- **Time Saved**: Estimated 70% reduction in development time compared to manual coding
- **Quality Improvements**: AI-generated tests caught edge cases (single asset validation, empty data handling)
- **Learning**: Developer learned `uv` package manager, GitHub Actions syntax, Render deployment through AI explanations

**Developer Control:**
- All AI-generated code was reviewed before committing
- Architecture decisions (FastAPI, React, Docker) were made by developer
- AI acted as an expert pair programmer, not an autonomous agent
- Developer iterated on prompts when initial outputs didn't meet requirements

### MCP (Model Context Protocol) Influence

While no custom MCP server was implemented for this project, the development workflow was influenced by MCP concepts:
- **Separation of Concerns**: Backend API acts as a "tool" that frontend can invoke (similar to MCP tool calling)
- **Structured Communication**: OpenAPI spec defines a strict contract between components (analogous to MCP resource schemas)
- **Stateless Interactions**: Each API call is independent, mirroring MCP's request-response pattern

---

## Technologies & Architecture

### System Architecture

```
┌─────────────────┐
│   User Browser  │
└────────┬────────┘
         │ HTTP
         ▼
┌─────────────────┐
│  React Frontend │  (Port 3000 dev / Port 8000 prod)
│  - Form UI      │
│  - Results View │
└────────┬────────┘
         │ POST /analyze
         ▼
┌─────────────────┐
│ FastAPI Backend │  (Port 8000)
│  - /health      │
│  - /analyze     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Data Layer     │
│  - yfinance API │
│  - Mock fallback│
└─────────────────┘
```

**Component Roles:**

- **Frontend (React)**
  - User interface and interaction
  - Form validation (client-side)
  - API communication via `fetch`
  - Results visualization

- **Backend (FastAPI)**
  - RESTful API endpoints
  - Input validation (Pydantic models)
  - Business logic orchestration
  - Automatic OpenAPI documentation

- **Data Fetching Layer**
  - `yfinance` library for Yahoo Finance API
  - Timezone normalization for pandas indices
  - Graceful degradation to mock data

- **Testing Strategy**
  - **Unit Tests**: Backend (pytest), Frontend (Jest/React Testing Library)
  - **Integration Tests**: Docker container with curl-based endpoint validation
  - **CI/CD**: Automated testing on every push/PR

- **Containerization**
  - Multi-stage Dockerfile (Node build → Python runtime)
  - Unified image serves both frontend static files and backend API
  - Production-ready with single `docker run` command

- **CI/CD (GitHub Actions)**
  - Parallel unit test jobs (backend + frontend)
  - Sequential integration test (Docker build + endpoint tests)
  - Conditional deployment to Render (main branch only)

- **Deployment (Render)**
  - Platform-as-a-Service with Blueprint configuration
  - Automatic HTTPS, health checks, and scaling
  - Deploy hook integration with CI/CD

---

## Frontend

### Functionality

The React frontend (`frontend/src/App.js`) provides:
- **Input Form**: Comma-separated ticker input, investment horizon selector
- **Loading States**: Visual feedback during API calls
- **Results Display**:
  - Correlation matrix as HTML table
  - High R² pairs as styled list items
- **Error Handling**: Displays backend error messages to user

### Backend Call Centralization

All backend communication is centralized in the `handleSubmit` function:
```javascript
const response = await fetch('/analyze', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ isins: isinList, investment_horizon_years: horizon })
});
```

**Development Mode**: `package.json` includes `"proxy": "http://127.0.0.1:8000"` to forward API calls from port 3000 to backend port 8000.

**Production Mode**: Backend serves frontend static files, so `/analyze` is same-origin.

### Frontend Tests

**Location**: `frontend/src/App.test.js`

**Test Coverage**:
- Renders application title correctly
- (Default React tests for component mounting)

**Run Tests**:
```bash
cd frontend
npm test
```

Tests run automatically in CI/CD pipeline with `CI=true` environment variable.

---

## API Contract (OpenAPI)

### Automatic Generation

FastAPI automatically generates OpenAPI 3.0 specifications from:
- Pydantic models (request/response schemas)
- Type hints (parameter types)
- Docstrings (endpoint descriptions)

### Contract as Source of Truth

The OpenAPI spec (`backend/openapi.yaml`) serves as the **single source of truth** for:
- Frontend developers (what endpoints exist, what data to send)
- Backend developers (what responses to return)
- Integration tests (expected response structure)

### Accessing Swagger UI

When the backend is running:
1. Navigate to `http://127.0.0.1:8000/docs`
2. Interactive documentation allows testing endpoints directly
3. Schemas are displayed with example values

**Alternative**: ReDoc UI available at `http://127.0.0.1:8000/redoc`

---

## Backend

### Structure

```
backend/
├── main.py          # FastAPI app, endpoints, CORS, static file serving
├── models.py        # Pydantic schemas (PortfolioInput, AnalysisResult, AssetPair)
├── data.py          # Data fetching logic (yfinance + mock fallback)
├── analysis.py      # Statistical analysis (correlation, R² computation)
├── tests/
│   ├── conftest.py  # Pytest configuration
│   └── test_api.py  # API endpoint tests
└── pyproject.toml   # uv dependency management
```

### Main Endpoints

**GET `/health`**
- Returns: `{"status": "ok"}`
- Purpose: Readiness check for load balancers

**POST `/analyze`**
- Request: `{"isins": ["AAPL", "MSFT"], "investment_horizon_years": 1}`
- Response: `{"correlation_matrix": {...}, "high_r_squared_pairs": [...]}`
- Validation: Pydantic enforces `min_items=2` for ISINs

### OpenAPI Contract Compliance

Backend strictly follows the OpenAPI contract:
- Pydantic models ensure request/response structure matches spec
- FastAPI raises 422 for validation errors (per OpenAPI spec)
- Response models are enforced via `response_model=AnalysisResult`

### Backend Tests

**Location**: `backend/tests/test_api.py`

**Test Coverage**:
1. `test_health`: Verifies `/health` returns 200 with correct JSON
2. `test_analyze_insufficient_assets`: Verifies validation error (422) for single asset
3. `test_analyze_mock_flow`: End-to-end test with mock tickers, validates response structure

**Run Tests**:
```bash
cd backend
uv run python -m pytest tests/ -v
```

Tests use FastAPI's `TestClient` for in-memory HTTP requests (no actual server required).

---

## Data & Persistence

### No Database Required

This application **does not use a database**. All data is:
- Fetched on-demand from Yahoo Finance API
- Processed in-memory (pandas DataFrames)
- Returned immediately to the client

### Rationale

**Why No Persistence?**
1. **Stateless Analysis**: Each request is independent; no user accounts or saved portfolios
2. **Fresh Data**: Financial data changes constantly; caching would require complex invalidation
3. **Simplicity**: Eliminates database setup, migrations, and connection management
4. **Scalability**: Stateless design allows horizontal scaling without shared state

**When Database Would Be Needed:**
- User authentication and saved portfolio lists
- Historical analysis tracking over time
- Caching expensive computations for frequently-requested ticker combinations

---

## Containerization

### Unified Docker Image

The project uses a **multi-stage Dockerfile** to build a single production image:

**Stage 1 (Build Frontend)**:
```dockerfile
FROM node:20-alpine as build-frontend
WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build
```

**Stage 2 (Backend + Static Files)**:
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ .
COPY --from=build-frontend /app/build /app/static
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Running with Docker

**Build**:
```bash
docker build -t portfolio-unified .
```

**Run**:
```bash
docker run -p 8000:8000 portfolio-unified
```

**Access**: Navigate to `http://localhost:8000` (both frontend and API served from same port)

### Separate Containers (Development)

For development, separate Dockerfiles exist:
- `backend/Dockerfile`: Backend only (port 8000)
- `frontend/Dockerfile`: Frontend only (port 3000)

---

## Integration Testing

### Test Coverage

Integration tests verify the **entire system** running in a Docker container:

**Workflow** (`.github/workflows/ci-cd.yml`):
1. Build Docker image from Dockerfile
2. Start container on port 8000
3. Wait 10 seconds for startup
4. Test `/health` endpoint (expect 200 OK)
5. Test `/analyze` endpoint with mock data (expect valid JSON response)
6. Verify response contains `correlation_matrix` field
7. Clean up container

### What This Validates

- **Build Process**: Dockerfile correctly assembles all components
- **Runtime Environment**: Container starts successfully
- **API Availability**: Endpoints are accessible
- **Data Processing**: Backend can fetch data and compute results
- **Response Format**: JSON structure matches expected schema

### Running Locally

```bash
docker build -t portfolio-test .
docker run -d -p 8000:8000 --name test-container portfolio-test
sleep 10
curl http://localhost:8000/health
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"isins": ["FAKE1", "FAKE2"], "investment_horizon_years": 1}'
docker stop test-container && docker rm test-container
```

---

## CI/CD Pipeline

### GitHub Actions Workflow

**File**: `.github/workflows/ci-cd.yml`

**Triggers**:
- Push to `main` branch
- Pull requests to `main`

### Pipeline Stages

**1. Test Backend** (Parallel)
- Install `uv` package manager
- Sync dependencies (`uv sync`)
- Run pytest (`uv run python -m pytest tests/ -v`)

**2. Test Frontend** (Parallel)
- Setup Node.js 20
- Install dependencies (`npm ci`)
- Run tests (`npm test -- --passWithNoTests`)

**3. Integration Tests** (Sequential, after unit tests pass)
- Build Docker image
- Start container
- Test `/health` and `/analyze` endpoints
- Clean up

**4. Deploy to Render** (Sequential, after integration tests pass)
- **Condition**: Only on push to `main` (not PRs)
- Trigger Render deploy hook via `curl`
- Requires `RENDER_DEPLOY_HOOK_URL` secret in GitHub

### Behavior

| Event | Unit Tests | Integration Tests | Deploy |
|-------|------------|-------------------|--------|
| Push to `main` | ✅ Run | ✅ Run | ✅ Deploy if tests pass |
| Pull Request | ✅ Run | ✅ Run | ❌ Skip |
| Push to other branch | ❌ Skip | ❌ Skip | ❌ Skip |

### Setup Instructions

See `.github/CI_CD_SETUP.md` for detailed instructions on configuring the `RENDER_DEPLOY_HOOK_URL` secret.

---

## Deployment

### Cloud Provider: Render

**Platform**: [Render.com](https://render.com) (Platform-as-a-Service)

**Deployment Method**: Blueprint (`render.yaml`)

**Configuration**:
```yaml
services:
  - type: web
    name: portfolio-collinearity-analyzer
    env: docker
    region: frankfurt
    plan: free
    dockerContext: .
    dockerfilePath: Dockerfile
    envVars:
      - key: PORT
        value: 8000
    autoDeploy: false  # Controlled by CI/CD
```

### Live Application

**URL**: [https://portfolio-collinearity-analyzer.onrender.com](https://portfolio-collinearity-analyzer.onrender.com)

**Note**: The free tier on Render may experience cold starts (15-30 second delay on first request after inactivity).

### Deployment Process

**Automatic (via CI/CD)**:
1. Push to `main` branch
2. GitHub Actions runs tests
3. If tests pass, triggers Render deploy hook
4. Render builds Docker image
5. Render deploys new version with zero-downtime

**Manual (via Render Dashboard)**:
1. Go to Render Dashboard
2. Select "New" → "Blueprint"
3. Connect GitHub repository
4. Render auto-detects `render.yaml`
5. Click "Apply"

### Reproducibility

To deploy to your own Render account:
1. Fork this repository
2. Create Render account
3. Follow "Blueprint" method above
4. (Optional) Configure GitHub Actions secret for automated deployments

---

## Reproducibility

### Run Locally (Development Mode)

**Backend**:
```bash
cd backend
uv sync
uv run uvicorn main:app --reload
# Access API at http://127.0.0.1:8000
# View docs at http://127.0.0.1:8000/docs
```

**Frontend** (separate terminal):
```bash
cd frontend
npm install
npm start
# Access UI at http://localhost:3000
```

### Run Tests

**Backend Tests**:
```bash
cd backend
uv run python -m pytest tests/ -v
```

**Frontend Tests**:
```bash
cd frontend
npm test
```

**Integration Tests** (requires Docker):
```bash
docker build -t portfolio-test .
docker run -d -p 8000:8000 --name test-container portfolio-test
sleep 10
curl http://localhost:8000/health
docker stop test-container && docker rm test-container
```

### Build Containers

**Unified Production Image**:
```bash
docker build -t portfolio-unified .
docker run -p 8000:8000 portfolio-unified
# Access at http://localhost:8000
```

**Separate Development Images**:
```bash
# Backend only
docker build -t portfolio-backend -f backend/Dockerfile .
docker run -p 8000:8000 portfolio-backend

# Frontend only
docker build -t portfolio-frontend ./frontend
docker run -p 3000:3000 portfolio-frontend
```

### Deploy to Render

**Prerequisites**:
- GitHub account
- Render account (free tier available)

**Steps**:
1. Fork this repository to your GitHub account
2. Log in to Render Dashboard
3. Click "New" → "Blueprint"
4. Authorize GitHub access
5. Select your forked repository
6. Render detects `render.yaml` automatically
7. Click "Apply" to deploy

**Optional CI/CD Setup**:
1. In Render Dashboard, go to your service → Settings → Deploy Hook
2. Copy the Deploy Hook URL
3. In GitHub repository, go to Settings → Secrets → Actions
4. Add secret: `RENDER_DEPLOY_HOOK_URL` = (paste URL)
5. Push to `main` branch to trigger automated deployment

---

## Project Status & Limitations

### Current Limitations

**1. Data Source**
- **Issue**: Relies on `yfinance`, an unofficial Yahoo Finance API
- **Impact**: Subject to rate limiting, potential API changes, occasional data gaps
- **Production Alternative**: Bloomberg API, FactSet, or Quandl (paid services)

**2. Analysis Method**
- **Issue**: Uses simple Pearson correlation on daily returns
- **Limitation**: Doesn't capture non-linear relationships or time-varying correlations
- **Missing**: Cointegration tests (Engle-Granger), rolling window correlations

**3. Scalability**
- **Issue**: Synchronous processing in single-threaded Python
- **Impact**: Large portfolios (100+ assets) may cause slow response times
- **Solution**: Implement async processing with Celery/Redis task queue

**4. No User Persistence**
- **Issue**: No database; users cannot save portfolios or view historical analyses
- **Impact**: Limited to one-off analyses
- **Future**: Add user authentication and portfolio tracking

### Realistic Future Improvements

**Short-term** (1-2 weeks):
- Add rolling window correlation charts (time-series visualization)
- Implement caching for frequently-requested ticker combinations
- Add more statistical tests (Spearman rank correlation, Kendall tau)

**Medium-term** (1-2 months):
- Implement cointegration analysis for pairs trading signals
- Add user authentication and saved portfolio lists
- Create PDF report generation for analysis results

**Long-term** (3-6 months):
- Build ML model to predict correlation regime changes
- Add factor analysis (PCA) to identify common risk factors
- Implement real-time WebSocket updates for live market data

### Known Issues

- **Timezone Handling**: Fixed in current version, but earlier versions had pandas timezone-aware index mismatches
- **SQLite Locking**: Resolved by disabling yfinance multi-threading in Docker containers
- **Frontend Test Coverage**: Minimal (1 test); should add component-level tests

---

## License

This project is open-source and available under the MIT License. Feel free to fork and improve!

---

## Acknowledgments

Developed as the final project for **AI Dev Tools Zoomcamp** to demonstrate practical application of AI-assisted software engineering workflows.