'use client';

import React, { useEffect, useState } from 'react';
import { useForm } from 'react-hook-form';
import api from '@/lib/api';
import { Input } from '@/components/ui/Input';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Loading } from '@/components/ui/Loading';

export default function IcpPage() {
  const { register, handleSubmit, setValue } = useForm();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState({ text: '', type: '' });

  useEffect(() => {
    const fetchIcp = async () => {
      try {
        const res = await api.get('/icp/');
        if (res.data) {
          setValue('industries', res.data.industries.join(', '));
          setValue('company_sizes', res.data.company_sizes.join(', '));
          setValue('job_titles', res.data.job_titles.join(', '));
          setValue('locations', res.data.locations.join(', '));
          setValue('revenue_range', res.data.revenue_range || '');
          setValue('custom_criteria', res.data.custom_criteria.join(', '));
          setValue('deal_breakers', res.data.deal_breakers.join(', '));
        }
      } catch (error) {
        console.error('Error fetching ICP:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchIcp();
  }, [setValue]);

  const onSubmit = async (data: any) => {
    try {
      setSaving(true);
      setMessage({ text: '', type: '' });
      
      const payload = {
        industries: data.industries.split(',').map((i: string) => i.trim()).filter(Boolean),
        company_sizes: data.company_sizes.split(',').map((i: string) => i.trim()).filter(Boolean),
        job_titles: data.job_titles.split(',').map((i: string) => i.trim()).filter(Boolean),
        locations: data.locations.split(',').map((i: string) => i.trim()).filter(Boolean),
        revenue_range: data.revenue_range,
        custom_criteria: data.custom_criteria.split(',').map((i: string) => i.trim()).filter(Boolean),
        deal_breakers: data.deal_breakers.split(',').map((i: string) => i.trim()).filter(Boolean),
      };

      await api.post('/icp/configure', payload);
      setMessage({ text: 'ICP configurado com sucesso!', type: 'success' });
    } catch (err) {
      setMessage({ text: 'Erro ao salvar configurações.', type: 'error' });
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <Loading fullScreen />;

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Perfil de Cliente Ideal (ICP)</h1>
        <p className="text-sm text-gray-500 mt-1">Configure os parâmetros para que a IA avalie o fit dos seus leads com precisão.</p>
      </div>
      
      <Card>
        <CardContent className="pt-6">
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            {message.text && (
              <div className={`p-3 rounded text-sm ${message.type === 'success' ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'}`}>
                {message.text}
              </div>
            )}

            <div className="space-y-4">
              <Input
                label="Setores de Atuação (separados por vírgula)"
                {...register('industries')}
                placeholder="ex: Tecnologia, Varejo, Saúde"
              />
              <Input
                label="Tamanhos de Empresa (separados por vírgula)"
                {...register('company_sizes')}
                placeholder="ex: 11-50, 51-200, Enterprise"
              />
              <Input
                label="Cargos Alvo (separados por vírgula)"
                {...register('job_titles')}
                placeholder="ex: CEO, Diretor de Vendas, CTO"
              />
              <Input
                label="Localizações Alvo (separados por vírgula)"
                {...register('locations')}
                placeholder="ex: São Paulo, Brasil, LATAM"
              />
              <Input
                label="Faixa de Faturamento Ideal"
                {...register('revenue_range')}
                placeholder="ex: R$ 1M - R$ 10M/ano"
              />
              
              <div className="border-t pt-4 mt-2">
                <h3 className="text-md font-medium mb-3">Critérios Avançados da IA</h3>
                <Input
                  label="Critérios Positivos Customizados (separados por vírgula)"
                  {...register('custom_criteria')}
                  placeholder="ex: Usa AWS, Crescimento acelerado, Recebeu aporte recente"
                />
                <Input
                  label="Deal Breakers - Impeditivos (separados por vírgula)"
                  {...register('deal_breakers')}
                  placeholder="ex: Recuperação judicial, Foco B2C exclusivo"
                />
              </div>
            </div>

            <div className="flex justify-end border-t pt-4">
              <Button type="submit" isLoading={saving}>
                Salvar Configuração ICP
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
