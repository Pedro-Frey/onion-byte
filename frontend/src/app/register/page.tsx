'use strict';
'use client';

import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Input } from '@/components/ui/Input';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { register as registerUser } from '@/lib/auth';
import { validateEmail, sanitizeInput } from '@/lib/security';
import { Zap } from 'lucide-react';

export default function RegisterPage() {
  const { register, handleSubmit, formState: { errors } } = useForm();
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const onSubmit = async (data: any) => {
    try {
      setLoading(true);
      setError('');
      
      const cleanEmail = sanitizeInput(data.email);
      const cleanCompanyName = sanitizeInput(data.company_name);
      
      if (!validateEmail(cleanEmail)) {
        setError('E-mail inválido');
        setLoading(false);
        return;
      }

      await registerUser(cleanEmail, data.password, cleanCompanyName);
      
      // Redirect to login with success message
      router.push('/login?registered=true');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erro ao registrar. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <Card className="max-w-md w-full space-y-8">
        <CardHeader className="text-center">
          <div className="flex justify-center text-blue-600 mb-4">
            <Zap className="h-10 w-10" />
          </div>
          <CardTitle className="text-2xl font-bold">Crie sua conta</CardTitle>
        </CardHeader>
        <CardContent>
          <form className="space-y-6" onSubmit={handleSubmit(onSubmit)}>
            {error && (
              <div className="bg-red-50 text-red-700 p-3 rounded-md text-sm">
                {error}
              </div>
            )}
            
            <div className="space-y-4">
              <Input
                label="Nome da Empresa"
                type="text"
                {...register('company_name', { required: 'Nome da empresa é obrigatório' })}
                error={errors.company_name?.message as string}
                placeholder="Sua Empresa Ltda"
              />

              <Input
                label="E-mail"
                type="email"
                {...register('email', { required: 'E-mail é obrigatório' })}
                error={errors.email?.message as string}
                placeholder="seu@email.com"
              />
              
              <Input
                label="Senha"
                type="password"
                {...register('password', { 
                  required: 'Senha é obrigatória',
                  minLength: { value: 6, message: 'Mínimo de 6 caracteres' }
                })}
                error={errors.password?.message as string}
                placeholder="••••••••"
                sanitize={false}
              />
            </div>

            <Button type="submit" className="w-full" isLoading={loading}>
              Registrar
            </Button>
            
            <div className="text-center text-sm">
              <span className="text-gray-600">Já tem uma conta? </span>
              <Link href="/login" className="font-medium text-blue-600 hover:text-blue-500">
                Faça login
              </Link>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
