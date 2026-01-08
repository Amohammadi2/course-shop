import { render, screen } from '@testing-library/react';
import Header from '../Header';

jest.mock('@/hooks/useAuth', () => ({
  useAuth: () => ({ isAuthenticated: false }),
}));

jest.mock('@/hooks/useWallet', () => ({
  useWallet: () => ({ balance: 0 }),
}));

describe('Header', () => {
  it('renders login and register links when not authenticated', () => {
    render(<Header />);

    expect(screen.getByText('Login')).toBeInTheDocument();
    expect(screen.getByText('Register')).toBeInTheDocument();
  });
});
