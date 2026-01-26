# Portfolio Collinearity Analyzer - Frontend

Minimal React frontend for the Portfolio Collinearity Analyzer.

## Prerequisites
- Node.js and npm installed.
- Backend running on `http://127.0.0.1:8000`.

## Installation

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

## Usage

1. Start the development server:
   ```bash
   npm start
   ```

2. Open [http://localhost:3000](http://localhost:3000) in your browser.

3. **Analyze**:
   - Enter comma-separated ISINs or Tickers (e.g., `AAPL, MSFT, GOOG`).
   - Set investment horizon.
   - Click "Analyze".
   - View the Correlation Matrix and High $R^2$ Pairs.
