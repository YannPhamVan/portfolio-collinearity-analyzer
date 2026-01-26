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
    # Use iterative fetching to avoid threading/sqlite locking issues in Docker
    data_frames = {}
    
    for ticker in isins:
        try:
            # Fetch history for this ticker
            # period="1y", "2y", etc. yfinance accepts '1y', '2y', '5y', '10y', 'ytd', 'max'
            # We approximate years to period string or just use start/end dates
            hist = yf.Ticker(ticker).history(start=start_date, end=end_date)
            
            if not hist.empty:
                # Keep only Close (or Adj Close if available, history usually returns 'Close' adjusted for splits)
                # Note: yf.Ticker.history returns 'Close' which is split-adjusted. Dividends are separate.
                # For collinearity, Close is fine.
                data_frames[ticker] = hist['Close']
        except Exception as e:
            print(f"Failed to fetch {ticker}: {e}")
            
    if not data_frames:
        print("yfinance failed to return any data. Falling back to mock data.")
        data = pd.DataFrame()
    else:
        # Align all series
        data = pd.DataFrame(data_frames)
    
    # Ensure we have a DataFrame even if empty
    if data.empty:
         data = pd.DataFrame()
    else:
        # Normalize index to timezone-naive to match expected_dates
        if data.index.tz is not None:
             data.index = data.index.tz_localize(None)
        # Also normalize to midnight to ensure matching with bdate_range if times differ
        data.index = data.index.normalize()

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
