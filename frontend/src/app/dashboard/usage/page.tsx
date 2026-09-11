'use client';

import React, { useEffect, useState } from 'react';
import api from '@/lib/api';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Loading } from '@/components/ui/Loading';

export default function UsagePage() {
  const [usage, setUsage] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUsage = async () => {
      try {
        const res = await api.get('/usage');
        setUsage(res.data);
      } catch (error) {
        console.error('Error fetching usage:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchUsage();
  }, []);

  if (loading) return <Loading fullScreen />;
  if (!usage) return <div>Erro ao carregar dados de uso.</div>;

  const percentage = Math.min(100, Math.round((usage.requests_used / usage.requests_limit) * 100)) || 0;
  const isNearLimit = percentage >= 80;

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold text-gray-900">Uso e Plano</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Plano Atual</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-blue-600 mb-2 uppercase">
              {usage.plan || 'Free'}
            </div>
            <p className="text-gray-500 text-sm">Atualize seu plano para limites maiores.</p>
            <button className="mt-4 px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-800 text-sm font-medium rounded-md w-full transition-colors">
              Fazer Upgrade
            </button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Consumo (Mês Atual)</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex justify-between text-sm mb-2">
              <span className="text-gray-600">Enriquecimentos realizados</span>
              <span className="font-medium text-gray-900">{usage.requests_used} / {usage.requests_limit}</span>
            </div>
            
            <div className="w-full bg-gray-200 rounded-full h-2.5 mb-2">
              <div 
                className={`h-2.5 rounded-full ${isNearLimit ? 'bg-red-500' : 'bg-blue-600'}`}
                style={{ width: `${percentage}%` }}
              ></div>
            </div>
            
            <p className="text-xs text-gray-500 text-right">{percentage}% utilizado</p>
            
            {isNearLimit && (
              <div className="mt-4 p-3 bg-red-50 text-red-700 text-sm rounded-md border border-red-100">
                Você está próximo do limite do seu plano atual. Considere fazer o upgrade.
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
