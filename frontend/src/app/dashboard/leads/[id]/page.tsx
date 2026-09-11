'use client';

import React, { useEffect, useState } from 'react';
import api from '@/lib/api';
import { Loading } from '@/components/ui/Loading';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { ScoreDetailedDisplay } from '@/components/ScoreDisplay';
import { ArrowLeft } from 'lucide-react';
import Link from 'next/link';

export default function LeadDetailPage({ params }: { params: { id: string } }) {
  const [lead, setLead] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchLead = async () => {
      try {
        const res = await api.get(`/leads/${params.id}`);
        setLead(res.data);
      } catch (error) {
        console.error('Error fetching lead details:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchLead();
  }, [params.id]);

  if (loading) return <Loading fullScreen />;
  if (!lead) return <div>Lead não encontrado.</div>;

  return (
    <div className="space-y-6 max-w-5xl">
      <div className="flex items-center gap-4 mb-2">
        <Link href="/dashboard/leads" className="text-gray-500 hover:text-gray-700">
          <ArrowLeft className="h-5 w-5" />
        </Link>
        <h1 className="text-2xl font-bold text-gray-900">{lead.nome}</h1>
        <Badge variant={lead.status === 'ENRIQUECIDO' ? 'success' : lead.status === 'ERRO' ? 'error' : 'warning'}>
          {lead.status}
        </Badge>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="md:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Dados Originais</CardTitle>
            </CardHeader>
            <CardContent>
              <dl className="grid grid-cols-1 sm:grid-cols-2 gap-x-4 gap-y-6">
                <div>
                  <dt className="text-sm font-medium text-gray-500">Email</dt>
                  <dd className="mt-1 text-sm text-gray-900">{lead.email}</dd>
                </div>
                <div>
                  <dt className="text-sm font-medium text-gray-500">Empresa</dt>
                  <dd className="mt-1 text-sm text-gray-900">{lead.empresa}</dd>
                </div>
                {lead.telefone && (
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Telefone</dt>
                    <dd className="mt-1 text-sm text-gray-900">{lead.telefone}</dd>
                  </div>
                )}
                {lead.linkedin_url && (
                  <div>
                    <dt className="text-sm font-medium text-gray-500">LinkedIn</dt>
                    <dd className="mt-1 text-sm text-blue-600 hover:underline">
                      <a href={lead.linkedin_url} target="_blank" rel="noopener noreferrer">Ver Perfil</a>
                    </dd>
                  </div>
                )}
              </dl>
            </CardContent>
          </Card>

          {lead.enriched_data && (
            <Card>
              <CardHeader>
                <CardTitle>Dados Enriquecidos</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-6">
                  {lead.enriched_data.company_info && (
                    <div>
                      <h4 className="text-sm font-semibold text-gray-900 mb-3 border-b pb-2">Informações da Empresa</h4>
                      <dl className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        {Object.entries(lead.enriched_data.company_info).map(([key, value]) => (
                          <div key={key}>
                            <dt className="text-xs font-medium text-gray-500 uppercase">{key.replace('_', ' ')}</dt>
                            <dd className="mt-1 text-sm text-gray-900">{String(value)}</dd>
                          </div>
                        ))}
                      </dl>
                    </div>
                  )}
                  {lead.enriched_data.social_profiles && lead.enriched_data.social_profiles.length > 0 && (
                    <div>
                      <h4 className="text-sm font-semibold text-gray-900 mb-2">Redes Sociais Encontradas</h4>
                      <ul className="list-disc pl-5 space-y-1">
                        {lead.enriched_data.social_profiles.map((profile: string, idx: number) => (
                          <li key={idx} className="text-sm text-blue-600"><a href={profile} target="_blank" rel="noopener noreferrer">{profile}</a></li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          )}
        </div>

        <div className="md:col-span-1">
          <Card className="h-full">
            <CardHeader>
              <CardTitle>Score e Análise</CardTitle>
            </CardHeader>
            <CardContent>
              {lead.score_data ? (
                <ScoreDetailedDisplay data={lead.score_data} />
              ) : (
                <div className="text-center py-6 text-gray-500">
                  <p>Score ainda não calculado.</p>
                  <p className="text-xs mt-1">Status: {lead.status}</p>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
