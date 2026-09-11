'use client';

import React, { useEffect, useState } from 'react';
import api from '@/lib/api';
import { LeadCard } from '@/components/LeadCard';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/Table';
import { Badge } from '@/components/ui/Badge';
import { Loading } from '@/components/ui/Loading';
import { useRouter } from 'next/navigation';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function DashboardPage() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const [statsRes, leadsRes] = await Promise.all([
          api.get('/leads/stats'),
          api.get('/leads?size=5')
        ]);
        setData({
          stats: statsRes.data,
          recentLeads: leadsRes.data.items || []
        });
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchDashboard();
  }, []);

  if (loading) return <Loading fullScreen />;
  if (!data) return <div>Erro ao carregar dados do dashboard.</div>;

  const chartData = [
    { name: 'Score A', count: data.stats?.by_grade?.A || 0, fill: '#22c55e' },
    { name: 'Score B', count: data.stats?.by_grade?.B || 0, fill: '#3b82f6' },
    { name: 'Score C', count: data.stats?.by_grade?.C || 0, fill: '#eab308' },
    { name: 'Score D', count: data.stats?.by_grade?.D || 0, fill: '#f97316' },
    { name: 'Score F', count: data.stats?.by_grade?.F || 0, fill: '#ef4444' },
  ];

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Visão Geral</h1>
      
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <LeadCard 
          title="Total de Leads" 
          value={data.stats?.total_leads || 0} 
        />
        <LeadCard 
          title="Leads Score A" 
          value={data.stats?.by_grade?.A || 0} 
        />
        <LeadCard 
          title="Leads Score B/C" 
          value={(data.stats?.by_grade?.B || 0) + (data.stats?.by_grade?.C || 0)} 
        />
        <LeadCard 
          title="Taxa de Enriquecimento" 
          value={`${data.stats?.enrichment_rate || 0}%`} 
        />
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Distribuição por Score</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="name" />
                <YAxis allowDecimals={false} />
                <Tooltip />
                <Bar dataKey="count" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-white rounded-lg border border-gray-200 shadow-sm overflow-hidden flex flex-col">
          <div className="p-6 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">Leads Recentes</h3>
          </div>
          <div className="flex-1 overflow-auto">
            <Table>
              <TableHeader>
                <TableHead>Nome</TableHead>
                <TableHead>Empresa</TableHead>
                <TableHead>Grade</TableHead>
              </TableHeader>
              <TableBody>
                {data.recentLeads.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={3} className="text-center py-4 text-gray-500">Nenhum lead encontrado</TableCell>
                  </TableRow>
                ) : (
                  data.recentLeads.map((lead: any) => (
                    <TableRow key={lead.id} onClick={() => router.push(`/dashboard/leads/${lead.id}`)}>
                      <TableCell className="font-medium text-gray-900">{lead.nome}</TableCell>
                      <TableCell>{lead.empresa}</TableCell>
                      <TableCell>
                        {lead.score_data ? (
                          <Badge variant={lead.score_data.grade}>{lead.score_data.grade}</Badge>
                        ) : (
                          <Badge variant="default">N/A</Badge>
                        )}
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </div>
        </div>
      </div>
    </div>
  );
}
