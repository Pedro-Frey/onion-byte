'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { 
  LayoutDashboard, 
  Users, 
  Zap, 
  Target, 
  Activity,
  LogOut
} from 'lucide-react';
import { logout } from '@/lib/auth';
import { cn } from '@/components/ui/Button';
import api from '@/lib/api';

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const [user, setUser] = useState<{email: string; company_name: string} | null>(null);

  useEffect(() => {
    // Fetch current user
    api.get('/users/me')
      .then(res => setUser(res.data))
      .catch(() => {
        // [DEV MODE] Ignora o erro e cria usuário falso
        setUser({ email: 'admin@onionbyte.com', company_name: 'Modo de Teste' });
      });
  }, [router]);

  const navItems = [
    { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
    { name: 'Leads', href: '/dashboard/leads', icon: Users },
    { name: 'Enriquecer', href: '/dashboard/enrich', icon: Zap },
    { name: 'Configurar ICP', href: '/dashboard/icp', icon: Target },
    { name: 'Uso & Plano', href: '/dashboard/usage', icon: Activity },
  ];

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Sidebar */}
      <div className="w-64 bg-white border-r border-gray-200 flex flex-col hidden md:flex">
        <div className="h-16 flex items-center px-6 border-b border-gray-200">
          <Zap className="h-6 w-6 text-blue-600 mr-2" />
          <span className="font-bold text-xl text-gray-900">Onion Byte</span>
        </div>
        
        <nav className="flex-1 px-4 py-6 space-y-1 overflow-y-auto">
          {navItems.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.name}
                href={item.href}
                className={cn(
                  'flex items-center px-3 py-2.5 text-sm font-medium rounded-md group transition-colors',
                  isActive 
                    ? 'bg-blue-50 text-blue-700' 
                    : 'text-gray-700 hover:text-gray-900 hover:bg-gray-100'
                )}
              >
                <item.icon 
                  className={cn(
                    'flex-shrink-0 h-5 w-5 mr-3',
                    isActive ? 'text-blue-700' : 'text-gray-400 group-hover:text-gray-500'
                  )} 
                />
                {item.name}
              </Link>
            );
          })}
        </nav>
        
        <div className="p-4 border-t border-gray-200">
          <div className="flex items-center mb-4 px-2">
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900 truncate">
                {user?.company_name || 'Carregando...'}
              </p>
              <p className="text-xs text-gray-500 truncate">
                {user?.email || ''}
              </p>
            </div>
          </div>
          <button
            onClick={() => logout()}
            className="flex items-center w-full px-3 py-2 text-sm font-medium text-gray-700 rounded-md hover:bg-gray-100 hover:text-gray-900 transition-colors"
          >
            <LogOut className="flex-shrink-0 h-5 w-5 mr-3 text-gray-400" />
            Sair
          </button>
        </div>
      </div>

      {/* Main content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        <main className="flex-1 overflow-y-auto bg-gray-50 p-6 md:p-8">
          {children}
        </main>
      </div>
    </div>
  );
}
