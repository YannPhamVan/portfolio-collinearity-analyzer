import React, { useState } from 'react';
import './App.css';

function App() {
  const [isins, setIsins] = useState("AAPL, MSFT, GOOG, TSLA");
  const [horizon, setHorizon] = useState(1);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    // Parse ISINs string into list
    const isinList = isins.split(',')
      .map(s => s.trim())
      .filter(s => s.length > 0);

    if (isinList.length < 2) {
      setError("Please provide at least 2 ISINs/Tickers.");
      setLoading(false);
      return;
    }

    try {
      const response = await fetch('/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          isins: isinList,
          investment_horizon_years: parseInt(horizon),
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Analysis failed");
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <h1>Portfolio Collinearity Analyzer</h1>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Assets (Comma Separated Tickers)</label>
          <textarea
            rows="3"
            value={isins}
            onChange={(e) => setIsins(e.target.value)}
            placeholder="e.g. AAPL, MSFT, GOOG"
          />
        </div>

        <div className="form-group">
          <label>Investment Horizon (Years)</label>
          <input
            type="number"
            min="1"
            max="10"
            value={horizon}
            onChange={(e) => setHorizon(e.target.value)}
          />
        </div>

        <button type="submit" disabled={loading}>
          {loading ? 'Analyzing...' : 'Analyze'}
        </button>
      </form>

      {error && <div className="error">Error: {error}</div>}

      {result && (
        <div className="results">
          {/* Correlation Matrix */}
          <h2>Correlation Matrix</h2>
          <div style={{ overflowX: 'auto' }}>
            <table>
              <thead>
                <tr>
                  <th></th>
                  {Object.keys(result.correlation_matrix).map(ticker => (
                    <th key={ticker}>{ticker}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {Object.keys(result.correlation_matrix).map(rowTicker => (
                  <tr key={rowTicker}>
                    <th>{rowTicker}</th>
                    {Object.keys(result.correlation_matrix).map(colTicker => (
                      <td key={colTicker}>
                        {result.correlation_matrix[rowTicker][colTicker]}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* High R2 Pairs */}
          <h2>High R² Pairs (&gt; 0.5)</h2>
          {result.high_r_squared_pairs.length === 0 ? (
            <p>No highly collinear pairs detected.</p>
          ) : (
            <ul>
              {result.high_r_squared_pairs.map((pair, idx) => (
                <li key={idx} className="pair-item">
                  <strong>{pair.asset_a}</strong> & <strong>{pair.asset_b}</strong>
                  <br />
                  Correlation: {pair.correlation} | R²: {pair.r_squared}
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
