import pandas as pd
import numpy as np
from typing import List, Dict
from models import AnalysisResult, AssetPair

def analyze_portfolio(prices_df: pd.DataFrame) -> AnalysisResult:
    """
    Computes correlation and R2 matrices from the prices DataFrame.
    Identifies pairs with R^2 > 0.5.
    """
    # Calculate daily returns
    returns_df = prices_df.pct_change().dropna()
    
    if returns_df.empty:
        # Fallback for empty data if enough history wasn't available for returns
        return AnalysisResult(correlation_matrix={}, high_r_squared_pairs=[])
        
    # Pearson correlation matrix
    corr_matrix = returns_df.corr(method='pearson')
    
    # R-squared matrix (coefficient of determination)
    r2_matrix = corr_matrix ** 2
    
    # Identify high R2 pairs
    high_r2_pairs = []
    
    # Iterate over the upper triangle of the matrix to avoid duplicates and self-comparison
    columns = corr_matrix.columns
    for i in range(len(columns)):
        for j in range(i + 1, len(columns)):
            asset_a = columns[i]
            asset_b = columns[j]
            
            r2 = r2_matrix.iloc[i, j]
            if r2 > 0.5:
                correlation = corr_matrix.iloc[i, j]
                pair = AssetPair(
                    asset_a=asset_a,
                    asset_b=asset_b,
                    correlation=round(correlation, 4),
                    r_squared=round(r2, 4)
                )
                high_r2_pairs.append(pair)
                
    # Sort pairs by R^2 descending
    high_r2_pairs.sort(key=lambda x: x.r_squared, reverse=True)
    
    # Convert correlation matrix to nested dict for JSON response
    # structure: { "AssetA": { "AssetB": 0.5, ... }, ... }
    corr_dict = corr_matrix.round(4).to_dict()
    
    return AnalysisResult(
        correlation_matrix=corr_dict,
        high_r_squared_pairs=high_r2_pairs
    )
