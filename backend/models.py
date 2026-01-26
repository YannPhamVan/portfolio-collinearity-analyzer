from typing import List, Dict
from pydantic import BaseModel, Field

class PortfolioInput(BaseModel):
    """
    Input model for portfolio analysis.
    """
    isins: List[str] = Field(..., min_items=2, description="List of ISIN codes or tickers to analyze.")
    investment_horizon_years: int = Field(1, ge=1, description="Investment horizon in years to fetch historical data.")

class AssetPair(BaseModel):
    """
    Represents a pair of assets and their correlation analysis.
    """
    asset_a: str
    asset_b: str
    correlation: float
    r_squared: float

class AnalysisResult(BaseModel):
    """
    Output model containing analysis results.
    """
    correlation_matrix: Dict[str, Dict[str, float]]
    high_r_squared_pairs: List[AssetPair]
