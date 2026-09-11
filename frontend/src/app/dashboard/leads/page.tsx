'use client';

import React, { useEffect, useState } from 'react';
import api from '@/lib/api';
import { useRouter } from 'next/navigation';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/Table';
import { Badge } from '@/components/ui/Badge';
import { Loading } from '@/components/ui/Loading';
import { Input } from '@/components/ui/Input';
import { Button } from '@/components/ui/Button';

export default function LeadsPage() {
  const [leads, setLeads] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const router = useRouter();

  useEffect(() => {
    fetchLeads();
  }, []);

  const fetchLeads = async (query = '') => {
    try {
      setLoading(true);
      const res = await api.get(`/leads?size=50${query ? `&search=${encodeURIComponent(query)}` : ''}`);
      setLeads(res.data.items || []);
    } catch (error) {
      console.error('Error fetching leads:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    fetchLeads(search);
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <h1 className="text-2xl font-bold text-gray-900">Leads</h1>
        <form onSubmit={handleSearch} className="flex gap-2 w-full sm:w-auto">
          <Input 
            placeholder="Buscar por nome ou empresa..." 
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full sm:w-64"
          />
          <Button type="submit">Buscar</Button>
        </form>
      </div>

      <div className="bg-white border border-gray-200 rounded-lg shadow-sm">
        {loading ? (
          <div className="py-12"><Loading /></div>
        ) : (
          <Table>
            <TableHeader>
              <TableHead>Nome</TableHead>
              <TableHead>Email</TableHead>
              <TableHead>Empresa</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Score</TableHead>
              <TableHead>Data</TableHead>
            </TableHeader>
            <TableBody>
              {leads.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={6} className="text-center py-8 text-gray-500">Nenhum lead encontrado.</TableCell>
                </TableRow>
              ) : (
                leads.map((lead) => (
                  <TableRow key={lead.id} onClick={() => router.push(`/dashboard/leads/${lead.id}`)}>
                    <TableCell className="font-medium text-gray-900">{lead.nome}</TableCell>
                    <TableCell>{lead.email}</TableCell>
                    <TableCell>{lead.empresa}</TableCell>
                    <TableCell>
                      <Badge variant={lead.status === 'ENRIQUECIDO' ? 'success' : lead.status === 'ERRO' ? 'error' : 'warning'}>
                        {lead.status}
                      </Badge>
                    </TableCell>
                    <TableCell>
                      {lead.score_data ? (
                        <div className="flex items-center gap-2">
                          <Badge variant={lead.score_data.grade}>{lead.score_data.grade}</Badge>
                          <span className="text-xs text-gray-500">{lead.score_data.score}</span>
                        </div>
                      ) : (
                        <span className="text-gray-400">-</span>
                      )}
                    </TableCell>
                    <TableCell className="text-gray-500 text-sm">
                      {new Date(lead.created_at).toLocaleDateString('pt-BR')}
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        )}
      </div>
    </div>
  );
}
