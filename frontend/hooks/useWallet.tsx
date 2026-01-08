'use client';

import {
  createContext,
  useContext,
  useState,
  useEffect,
  ReactNode,
} from 'react';
import api from '@/services/api';
import { useAuth } from './useAuth';

interface WalletContextType {
  balance: number;
  fetchBalance: () => void;
}

const WalletContext = createContext<WalletContextType | undefined>(undefined);

export const WalletProvider = ({ children }: { children: ReactNode }) => {
  const [balance, setBalance] = useState(0);
  const { isAuthenticated } = useAuth();

  const fetchBalance = async () => {
    if (isAuthenticated) {
      try {
        const response = await api.get('/wallet/balance/');
        setBalance(response.data.balance);
      } catch (error) {
        console.error('Failed to fetch wallet balance:', error);
      }
    }
  };

  useEffect(() => {
    fetchBalance();
  }, [isAuthenticated]);

  return (
    <WalletContext.Provider value={{ balance, fetchBalance }}>
      {children}
    </WalletContext.Provider>
  );
};

export const useWallet = () => {
  const context = useContext(WalletContext);
  if (context === undefined) {
    throw new Error('useWallet must be used within a WalletProvider');
  }
  return context;
};
