# Portfolio Collinearity Analyzer - Frontend

Minimal React frontend for the Portfolio Collinearity Analyzer.

Frontend communication with the backend is centralized through a dedicated API client, and the core workflow is covered by an integration-style frontend test.

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

## Architecture

The frontend follows a clean separation of concerns:
- **`src/api/client.js`**: Centralized API client for all backend communication.
- **`src/App.js`**: Main UI logic and state management, using the API client.
- **`src/App.css`**: Application styling.

## Testing

The project includes a comprehensive test suite covering the core analysis workflow.
To run tests:
```bash
npm test
```
The tests mock the backend API to ensure the UI behaves correctly under various conditions (success, error, validation).
