/**
 * API Client for Portfolio Collinearity Analyzer
 * 
 * Centralizes all backend API communication.
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || '';

/**
 * Analyzes a portfolio for collinearity
 * 
 * @param {Object} input - The analysis input
 * @param {string[]} input.isins - Array of ISINs/Tickers
 * @param {number} input.investment_horizon_years - Investment horizon in years
 * @returns {Promise<Object>} Analysis results containing correlation_matrix and high_r_squared_pairs
 * @throws {Error} If the API request fails
 */
export async function analyzePortfolio({ isins, investment_horizon_years }) {
  const response = await fetch(`${API_BASE_URL}/analyze`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      isins,
      investment_horizon_years,
    }),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `Analysis failed with status ${response.status}`);
  }

  return await response.json();
}
