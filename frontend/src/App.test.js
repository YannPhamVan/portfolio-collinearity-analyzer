import { render, screen } from '@testing-library/react';
import App from './App';

test('renders portfolio analyzer title', () => {
  render(<App />);
  const titleElement = screen.getByText(/Portfolio Collinearity Analyzer/i);
  expect(titleElement).toBeInTheDocument();
});
