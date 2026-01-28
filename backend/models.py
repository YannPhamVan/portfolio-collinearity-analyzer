from typing import Annotated
from pydantic import BaseModel, Field, field_validator

class PortfolioInput(BaseModel):
    """
    Input model for portfolio analysis.
    """
    isins: Annotated[list[str], Field(
        min_length=2, 
        description="List of unique ISIN codes or tickers to analyze."
    )]
    investment_horizon_years: Annotated[int, Field(
        default=1, 
        ge=1, 
        le=10,
        description="Investment horizon in years to fetch historical data."
    )]

    @field_validator('isins')
    @classmethod
    def validate_unique_isins(cls, v: list[str]) -> list[str]:
        if len(set(v)) < 2:
            raise ValueError("At least 2 unique ISINs/tickers are required.")
        return v

class AssetPair(BaseModel):
    """
    Represents a pair of assets and their correlation analysis.
    """
    asset_a: str = Field(description="Symbol of the first asset")
    asset_b: str = Field(description="Symbol of the second asset")
    correlation: float = Field(description="Pearson correlation coefficient")
    r_squared: float = Field(description="Coefficient of determination (R^2)")

class AnalysisResult(BaseModel):
    """
    Output model containing analysis results.
    """
    correlation_matrix: dict[str, dict[str, float]] = Field(
        description="Matrix of correlations (Asset -> Asset -> Correlation)"
    )
    high_r_squared_pairs: list[AssetPair] = Field(
        description="List of asset pairs with R^2 > 0.5"
    )
