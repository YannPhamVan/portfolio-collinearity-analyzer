import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from './App';
import * as apiClient from './api/client';

// Mock the API client module
jest.mock('./api/client');

describe('Portfolio Analysis Workflow', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    jest.clearAllMocks();
  });

  test('submits portfolio and renders analysis results', async () => {
    // Mock successful API response
    const mockResponse = {
      correlation_matrix: {
        'AAPL': { 'AAPL': '1.00', 'MSFT': '0.75' },
        'MSFT': { 'AAPL': '0.75', 'MSFT': '1.00' }
      },
      high_r_squared_pairs: [
        {
          asset_a: 'AAPL',
          asset_b: 'MSFT',
          correlation: '0.75',
          r_squared: '0.56'
        }
      ]
    };

    apiClient.analyzePortfolio.mockResolvedValue(mockResponse);

    // Render the App component
    render(<App />);

    // Verify initial state
    expect(screen.getByText('Portfolio Collinearity Analyzer')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /analyze/i })).toBeInTheDocument();

    // Fill in the form
    const textArea = screen.getByPlaceholderText(/e.g. AAPL, MSFT, GOOG/i);
    const horizonInput = screen.getByLabelText(/investment horizon/i);

    fireEvent.change(textArea, { target: { value: 'AAPL, MSFT' } });
    fireEvent.change(horizonInput, { target: { value: '2' } });

    // Submit the form
    const submitButton = screen.getByRole('button', { name: /analyze/i });
    fireEvent.click(submitButton);

    // Verify loading state
    expect(screen.getByText('Analyzing...')).toBeInTheDocument();

    // Verify API was called with correct parameters
    await waitFor(() => {
      expect(apiClient.analyzePortfolio).toHaveBeenCalledWith({
        isins: ['AAPL', 'MSFT'],
        investment_horizon_years: 2
      });
    });

    // Wait for results to be rendered
    await waitFor(() => {
      expect(screen.getByText('Correlation Matrix')).toBeInTheDocument();
    });

    // Verify correlation matrix is displayed
    expect(screen.getAllByText('AAPL').length).toBeGreaterThan(0);
    expect(screen.getAllByText('MSFT').length).toBeGreaterThan(0);

    // Verify high R² pairs section
    expect(screen.getByText(/High R² Pairs/i)).toBeInTheDocument();
    expect(screen.getAllByText(/0.75/).length).toBeGreaterThan(0);
    expect(screen.getAllByText(/0.56/).length).toBeGreaterThan(0);
  });

  test('displays error when API call fails', async () => {
    // Mock API error
    const errorMessage = 'Failed to fetch data';
    apiClient.analyzePortfolio.mockRejectedValue(new Error(errorMessage));

    render(<App />);

    // Fill in and submit form
    const textArea = screen.getByPlaceholderText(/e.g. AAPL, MSFT, GOOG/i);
    fireEvent.change(textArea, { target: { value: 'AAPL, MSFT' } });

    const submitButton = screen.getByRole('button', { name: /analyze/i });
    fireEvent.click(submitButton);

    // Wait for error to be displayed
    await waitFor(() => {
      expect(screen.getByText(`Error: ${errorMessage}`)).toBeInTheDocument();
    });

    // Verify no results are shown
    expect(screen.queryByText('Correlation Matrix')).not.toBeInTheDocument();
  });

  test('validates minimum number of ISINs', async () => {
    render(<App />);

    // Try to submit with only one ISIN
    const textArea = screen.getByPlaceholderText(/e.g. AAPL, MSFT, GOOG/i);
    fireEvent.change(textArea, { target: { value: 'AAPL' } });

    const submitButton = screen.getByRole('button', { name: /analyze/i });
    fireEvent.click(submitButton);

    // Verify error message
    await waitFor(() => {
      expect(screen.getByText(/Please provide at least 2 ISINs\/Tickers/i)).toBeInTheDocument();
    });

    // Verify API was not called
    expect(apiClient.analyzePortfolio).not.toHaveBeenCalled();
  });
});
