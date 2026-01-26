# Portfolio Collinearity Analyzer

A minimal FastAPI backend designed to detect redundant assets in financial portfolios by analyzing historical price correlations and coefficients of determination ($R^2$).

## Problem Statement
In portfolio management, **collinearity** (high correlation) between assets reduces diversification benefits and increases risk without necessarily increasing expected returns. Identifying these redundant pairs is crucial for constructing efficient portfolios.

## Methodology
The analyzer processes a list of ISINs/tickers and an investment horizon to:
1. **Fetch Data**: Retrieve historical daily adjusted close prices (via `yfinance`).
2. **Align Series**: Normalize time series to a common date index, handling missing data.
3. **Compute Correlations**: Calculate the Pearson correlation matrix for daily returns.
4. **Detect Redundancy**: Compute $R^2$ (Correlation squared) to measure how well one asset's movements explain another's. Pairs with $R^2 > 0.5$ are flagged.

## API Usage

### Endpoint: `GET /health`
Returns system status.
```json
{ "status": "ok" }
```

### Endpoint: `POST /analyze`

#### Request
```json
POST /analyze
{
  "isins": ["AAPL", "MSFT", "GOOG", "TSLA"],
  "investment_horizon_years": 1
}
```

#### Response
```json
{
  "correlation_matrix": {
    "AAPL": { "MSFT": 0.65, "GOOG": 0.55, ... },
    ...
  },
  "high_r_squared_pairs": [
    {
      "asset_a": "AAPL",
      "asset_b": "MSFT",
      "correlation": 0.65,
      "r_squared": 0.4225
    }
  ]
}
```

## Running Locally

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Start Server**:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

## Limitations & Future Improvements
- **Data Source**: relies on `yfinance` (unofficial Yahoo Finance API), which may be rate-limited or unstable.
- **Metric**: Currently uses simple Pearson correlation on daily returns. Future versions could include cointegration tests or rolling window correlations.
- **Performance**: Analysis is synchronous and in-memory; large portfolios may require async processing or optimized array operations.