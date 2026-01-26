from fastapi import FastAPI, HTTPException
from models import PortfolioInput, AnalysisResult
from data import fetch_historical_data
from analysis import analyze_portfolio

app = FastAPI(title="Portfolio Collinearity Analyzer", version="1.0.0")

@app.post("/analyze", response_model=AnalysisResult)
async def analyze_endpoint(payload: PortfolioInput):
    """
    Analyzes asset correlations and R-squared to detect redundancy.
    Input: List of ISINs/tickers and investment horizon.
    Output: Correlation matrix and list of pairs with R^2 > 0.5.
    """
    if len(set(payload.isins)) < 2:
        raise HTTPException(status_code=400, detail="At least 2 unique ISINs/tickers are required.")
    
    # Fetch data (real or mock)
    # Using 'tickers' as variable helper since we usually pass tickers to yfinance
    prices_df = fetch_historical_data(payload.isins, payload.investment_horizon_years)
    
    if prices_df.empty or prices_df.shape[1] < 2:
        raise HTTPException(status_code=500, detail="Insufficient data fetched for analysis.")
        
    # Analyze
    result = analyze_portfolio(prices_df)
    
    return result

if __name__ == "__main__":
    import uvicorn
    # Run the app locally
    uvicorn.run(app, host="0.0.0.0", port=8000)
