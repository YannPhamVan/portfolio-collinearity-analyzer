from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from models import PortfolioInput, AnalysisResult
from data import fetch_historical_data
from analysis import analyze_portfolio

app = FastAPI(
    title="Portfolio Collinearity Analyzer",
    description="API for detecting redundant financial assets using historical price correlations.",
    version="1.1.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", summary="Health Check")
async def health():
    """Returns the API status to verify connectivity."""
    return {"status": "ok"}

@app.post("/analyze", response_model=AnalysisResult, summary="Analyze Portfolio")
async def analyze_endpoint(payload: PortfolioInput):
    """
    Analyzes asset correlations and R-squared to detect redundancy.
    
    Validates that at least 2 unique tickers are provided and fetches historical data
    (or falls back to mock data if providers are unavailable).
    """
    # Note: Unique ISIN validation is now handled by Pydantic field_validator in PortfolioInput
    
    # Fetch data (real or mock)
    prices_df = fetch_historical_data(payload.isins, payload.investment_horizon_years)
    
    if prices_df.empty or prices_df.shape[1] < 2:
        raise HTTPException(
            status_code=500, 
            detail="Insufficient historical data could be gathered for the selected assets."
        )
        
    # Perform statistical analysis
    result = analyze_portfolio(prices_df)
    
    return result

# Serve frontend static assets if they exist
if os.path.exists("static"):
    app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
