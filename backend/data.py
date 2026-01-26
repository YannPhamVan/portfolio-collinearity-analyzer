import pandas as pd
import numpy as np
import yfinance as yf
from typing import List
from datetime import datetime, timedelta

def fetch_historical_data(isins: List[str], years: int) -> pd.DataFrame:
    """
    Fetches historical daily adjusted close prices for the given ISINs/tickers.
    If yfinance fails or returns empty data for a ticker, generates mock random walk data.
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365 * years)
    
    # Try fetching data with yfinance
    # yfinance expects space-separated tickers
    tickers_str = " ".join(isins)
    
    try:
        # download data
        data = yf.download(tickers_str, start=start_date, end=end_date, progress=False)['Adj Close']
        
        # If passed single ticker, yfinance returns Series, convert to DataFrame
        if isinstance(data, pd.Series):
            data = data.to_frame(name=isins[0])
            
        # Ensure we have all columns, even if some failed
        if data.empty:
             data = pd.DataFrame()
    except Exception as e:
        print(f"yfinance failed: {e}. Falling back to mock data for all assets.")
        data = pd.DataFrame()

    # Align to common index if sufficient data, otherwise rebuild index
    # We will ensure the dataframe covers the requested period with business days
    expected_dates = pd.bdate_range(start=start_date, end=end_date)
    
    # Reindex to full range to handle missing days (and fill NAs later or generated mock)
    # But for simplicity, we'll just check what's missing and fill/mock
    
    final_df = pd.DataFrame(index=expected_dates)
    
    for ticker in isins:
        if ticker in data.columns and not data[ticker].dropna().empty:
            # Reindex this ticker's data to our expected dates
            # Forward fill missing data (e.g. holidays differ) then backward fill
            series = data[ticker].reindex(expected_dates).ffill().bfill()
            final_df[ticker] = series
        else:
            # Generates mock random walk
            # Starting price 100, daily returns N(0, 0.01)
            # Seed based on ticker name hash for reproducibility
            np.random.seed(abs(hash(ticker)) % (2**32))
            returns = np.random.normal(0, 0.01, size=len(expected_dates))
            price_series = 100 * np.cumprod(1 + returns)
            final_df[ticker] = price_series
            
    # Drop any remaining NaNs if any (shouldn't be with the logic above)
    final_df = final_df.dropna()
    
    return final_df
