'use client';

import Link from 'next/link';
import { useAuth } from '@/hooks/useAuth';
import { useWallet } from '@/hooks/useWallet';

export default function Header() {
  const { isAuthenticated, logout } = useAuth();
  const { balance } = useWallet();

  return (
    <header className="bg-white shadow-md">
      <nav className="container flex items-center justify-between p-4 mx-auto">
        <Link href="/">
          <span className="text-xl font-bold">E-Learning</span>
        </Link>
        <div>
          {isAuthenticated ? (
            <div className="flex items-center space-x-4">
              <span className="font-bold">Balance: {balance} credits</span>
              <button
                onClick={logout}
                className="px-4 py-2 font-bold text-white bg-red-600 rounded-md hover:bg-red-700"
              >
                Logout
              </button>
            </div>
          ) : (
            <>
              <Link href="/login">
                <span className="px-4 py-2 font-bold">Login</span>
              </Link>
              <Link href="/register">
                <span className="px-4 py-2 font-bold text-white bg-indigo-600 rounded-md hover:bg-indigo-700">
                  Register
                </span>
              </Link>
            </>
          )}
        </div>
      </nav>
    </header>
  );
}
