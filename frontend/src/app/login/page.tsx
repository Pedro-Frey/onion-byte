'use strict';
'use client';

import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Input } from '@/components/ui/Input';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { login } from '@/lib/auth';
import { validateEmail, sanitizeInput } from '@/lib/security';
import { Zap } from 'lucide-react';

export default function LoginPage() {
  const { register, handleSubmit, formState: { errors } } = useForm();
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const onSubmit = async (data: any) => {
    try {
      setLoading(true);
      setError('');
      
      const cleanEmail = sanitizeInput(data.email);
      const cleanPassword = data.password; // Don't strip chars from password, just send it

      if (!validateEmail(cleanEmail)) {
        setError('E-mail inválido');
        setLoading(false);
        return;
      }

      await login(cleanEmail, cleanPassword);
      router.push('/dashboard');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erro ao realizar login. Verifique suas credenciais.');
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
          <CardTitle className="text-2xl font-bold">Acesse sua conta</CardTitle>
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
                sanitize={false} // Don't sanitize passwords on input to avoid breaking special chars
              />
            </div>

            <Button type="submit" className="w-full" isLoading={loading}>
              Entrar
            </Button>

            <Button 
              type="button" 
              className="w-full bg-green-600 hover:bg-green-700 mt-2" 
              onClick={() => {
                window.location.href = '/dashboard';
              }}
            >
              🚀 Pular Login (Ver Dashboard)
            </Button>
            
            <div className="text-center text-sm mt-4">
              <span className="text-gray-600">Não tem uma conta? </span>
              <Link href="/register" className="font-medium text-blue-600 hover:text-blue-500">
                Registre-se
              </Link>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
