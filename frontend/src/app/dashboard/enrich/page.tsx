'use client';

import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import api from '@/lib/api';
import { Input } from '@/components/ui/Input';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { maskCPF, maskPhone, validateEmail } from '@/lib/security';
import { useRouter } from 'next/navigation';

export default function EnrichPage() {
  const { register, handleSubmit, formState: { errors }, setValue, watch } = useForm();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const router = useRouter();

  const handleCpfChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setValue('cpf', maskCPF(e.target.value));
  };

  const handlePhoneChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setValue('telefone', maskPhone(e.target.value));
  };

  const onSubmit = async (data: any) => {
    try {
      setLoading(true);
      setError('');

      if (!validateEmail(data.email)) {
        setError('E-mail inválido');
        setLoading(false);
        return;
      }

      // Limpar campos vazios
      Object.keys(data).forEach(key => {
        if (data[key] === '') delete data[key];
      });

      const response = await api.post('/leads/enrich', data);
      router.push(`/dashboard/leads/${response.data.id}`);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erro ao enriquecer lead');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Enriquecer Novo Lead</h1>
      
      <Card>
        <CardHeader>
          <CardTitle>Dados Iniciais</CardTitle>
          <p className="text-sm text-gray-500">Insira os dados que você tem. Nossa IA buscará o resto.</p>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            {error && (
              <div className="bg-red-50 text-red-700 p-3 rounded text-sm">{error}</div>
            )}
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Input
                label="Nome *"
                {...register('nome', { required: 'Nome é obrigatório' })}
                error={errors.nome?.message as string}
                placeholder="João da Silva"
              />
              <Input
                label="E-mail *"
                type="email"
                {...register('email', { required: 'E-mail é obrigatório' })}
                error={errors.email?.message as string}
                placeholder="joao@empresa.com"
              />
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Input
                label="Empresa *"
                {...register('empresa', { required: 'Empresa é obrigatória' })}
                error={errors.empresa?.message as string}
                placeholder="Nome da Empresa"
              />
              <Input
                label="LinkedIn URL"
                {...register('linkedin_url')}
                placeholder="https://linkedin.com/in/..."
              />
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Input
                label="Telefone"
                {...register('telefone')}
                onChange={handlePhoneChange}
                placeholder="+55 (11) 99999-9999"
              />
              <Input
                label="CPF"
                {...register('cpf')}
                onChange={handleCpfChange}
                placeholder="000.000.000-00"
              />
            </div>
            
            <div className="pt-4 flex justify-end">
              <Button type="submit" isLoading={loading}>
                Enriquecer e Analisar
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
