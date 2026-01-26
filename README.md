# Portfolio Collinearity Analyzer

**Detect and visualize redundant assets in your financial portfolio.**

This project is a technical demonstration of a full-stack application that analyzes the collinearity between financial assets. By leveraging historical price data and statistical metrics (Correlation, $R^2$), it identifies asset pairs that move too similarly, helping investors improve diversification.

## Problem Statement

**True diversification means owning assets that behave differently.**
In portfolio management, adding more assets doesn't always reduce risk. If assets are highly correlated (collinear), they crash together. Identifying these redundant pairs is crucial for:
-   **Risk Reduction**: Avoiding concentrated exposure to specific market factors.
-   **Capital Efficiency**: Reallocating capital from redundant assets to complementary ones.

## Project Structure

-   `backend/`: **FastAPI** application. Handles data fetching (`yfinance`), statistical analysis, and API endpoints.
-   `frontend/`: **React** application. Provides a user-friendly interface to input tickers and visualize results.
-   `backend/openapi.yaml`: Complete **OpenAPI 3.0** specification of the backend API.

## Frontend (User Interface)

The frontend provides a simple form to submit your portfolio and view the Correlation Matrix and High $R^2$ Pairs.

### Installation & Run

1.  Navigate to the directory:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Start the application:
    ```bash
    npm start
    ```
4.  Open [http://localhost:3000](http://localhost:3000) in your browser.

### Usage
-   **Assets**: Enter comma-separated ISINs or Tickers (e.g., `AAPL, MSFT, GOOG, TSLA`).
-   **Horizon**: Select the number of years for historical data analysis.
-   **Analyze**: Click the button to fetch data and compute metrics.

## Backend (API Analysis)

The backend powers the analysis using Python's data science stack (`pandas`, `numpy`).

### Setup (with uv)

1.  Navigate to `backend/`:
    ```bash
    cd backend
    ```
2.  Install dependencies:
    ```bash
    uv sync
    ```

### Run Server

To start the API server:
```bash
uv run uvicorn main:app --reload
```
The server will run on `http://127.0.0.1:8000`.

### Key Endpoints

-   **GET** `/health`: Check readiness.
    -   *Response*: `{ "status": "ok" }`
-   **POST** `/analyze`: Perform collinearity analysis.
    -   *Request*: `{"isins": ["AAPL", "MSFT"], "investment_horizon_years": 1}`
    -   *Response*: Returns correlation matrix and flagged pairs.

## End-to-End Testing

To fully verify the system, run both components simultaneously:

1.  **Backend**: Running on port 8000.
2.  **Frontend**: Running on port 3000.

**Test Flow**:
1.  Open `http://localhost:3000`.
2.  Enter assets (e.g., `AAPL, MSFT`) and horizon (e.g., `1`).
3.  Click **Analyze**.
4.  Confirm that the Correlation Matrix table appears and values seem reasonable (e.g., correlation is between -1 and 1).
5.  *Independent Backend Check*: You can also verify the backend is responsive via Swagger UI at `http://localhost:8000/docs`.

## Containerization (Docker)

You can run each component in its own container.

### Backend

Create a `Dockerfile` in the root (or `backend/`) with:
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY backend/ .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Build & Run**:
```bash
docker build -t portfolio-backend -f backend/Dockerfile .
docker run -p 8000:8000 portfolio-backend
```

### Frontend

Create a `Dockerfile` in `frontend/` with:
```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY frontend/ .
RUN npm install
EXPOSE 3000
CMD ["npm", "start"]
```

**Build & Run**:
```bash
docker build -t portfolio-frontend ./frontend
docker run -p 3000:3000 portfolio-frontend
```

### Unified Container (Best for Deployment)

This builds both Frontend and Backend into a single lightweight image.

**Build & Run**:
```bash
docker build -t portfolio-unified .
docker run -p 8000:8000 portfolio-unified
```
Access the full app at `http://localhost:8000`.

## API Specifications

For developers, the full API contract is available in [backend/openapi.yaml](backend/openapi.yaml). You can also view interactive documentation at `http://127.0.0.1:8000/docs` when the server is running.

## Limitations & Future Improvements

-   **Data Fidelity**: Relies on `yfinance`, which is an unofficial API. Production systems would use paid providers (Bloomberg, FactSet).
-   **Analysis Method**: Currently uses Pearson correlation on daily returns.
    -   *Future*: Implement cointegration tests (Engle-Granger) for long-term pairs trading signals.
    -   *Future*: Add Rolling Window Correlation to see how relationships change over time.
-   **Scalability**: Processing is synchronous. For portfolios with 100+ assets, offloading to background tasks (Celery/Redis) would improve responsiveness.

## License

This project is open-source. Feel free to fork and improve!