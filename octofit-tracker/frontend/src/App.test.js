import { render, screen } from '@testing-library/react';
import App from './App';

test('renders OctoFit Tracker welcome message', () => {
  render(<App />);
  const headingElement = screen.getByText(/Welcome to OctoFit Tracker/i);
  expect(headingElement).toBeInTheDocument();
});
