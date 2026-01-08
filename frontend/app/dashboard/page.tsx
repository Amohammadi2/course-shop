"use client";
import withAuth from '@/app/components/withAuth/withAuth';
import { useAuth } from '@/app/contexts/AuthContext';
import { Button } from '@/components/ui/button';

function Dashboard() {
  const { user, logout } = useAuth();

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="text-center">
        <h1 className="text-3xl font-bold">Hello, {user?.username}!</h1>
        <Button onClick={logout} className="mt-4">Logout</Button>
      </div>
    </div>
  );
}

export default withAuth(Dashboard);
