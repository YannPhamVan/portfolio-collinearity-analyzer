# Portfolio Collinearity Analyzer API

This API provides tools to detect redundant assets in financial portfolios by analyzing historical price correlations and coefficients of determination ($R^2$).

## Run the Backend

Ensure you are in the `backend` directory and dependencies are installed.

```bash
cd backend
pip install -r ../requirements.txt
uvicorn main:app --reload
```
The server will start at `http://127.0.0.1:8000`.

## Endpoints

### 1. System Health Check
**GET** `/health`

Returns the operational status of the API.

**Response (200 OK):**
```json
{
  "status": "ok"
}
```

### 2. Analyze Portfolio
**POST** `/analyze`

Analyzes a list of assets for collinearity over a specified investment horizon.

**Request Body:**
```json
{
  "isins": ["AAPL", "MSFT", "GOOG"],
  "investment_horizon_years": 1
}
```

**Response (200 OK):**
```json
{
  "correlation_matrix": {
    "AAPL": {
      "MSFT": 0.65,
      "GOOG": 0.55
    },
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

## Testing with Swagger UI

FastAPI provides interactive documentation automatically.

1. Start the server.
2. Open your browser to: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
3. You can execute requests directly from this interface.

## Testing with Curl

```bash
curl -X POST "http://127.0.0.1:8000/analyze" \
     -H "Content-Type: application/json" \
     -d '{"isins": ["AAPL", "MSFT"], "investment_horizon_years": 1}'
```
