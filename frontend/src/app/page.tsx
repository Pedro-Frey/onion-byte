'use client';

import Link from 'next/link';
import { Button } from '@/components/ui/Button';
import { ShieldCheck, Zap, Database } from 'lucide-react';

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-white">
      <header className="absolute inset-x-0 top-0 z-50">
        <nav className="flex items-center justify-between p-6 lg:px-8" aria-label="Global">
          <div className="flex lg:flex-1">
            <a href="#" className="-m-1.5 p-1.5 font-bold text-xl text-blue-600 flex items-center gap-2">
              <Zap className="h-6 w-6" /> Onion Byte
            </a>
          </div>
          <div className="flex flex-1 justify-end gap-x-4">
            <Link href="/login">
              <Button variant="ghost">Login</Button>
            </Link>
            <Link href="/register">
              <Button variant="primary">Registrar</Button>
            </Link>
          </div>
        </nav>
      </header>

      <main className="isolate">
        {/* Hero section */}
        <div className="relative pt-14">
          <div className="py-24 sm:py-32 lg:pb-40">
            <div className="mx-auto max-w-7xl px-6 lg:px-8 text-center">
              <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">
                Enriquecimento de Leads com Inteligência
              </h1>
              <p className="mt-6 text-lg leading-8 text-gray-600 max-w-2xl mx-auto">
                Transforme e-mails básicos em perfis completos. O Onion Byte enriquece seus leads, pontua o fit da empresa e otimiza sua conversão com segurança e rapidez.
              </p>
              <div className="mt-10 flex items-center justify-center gap-x-6">
                <Link href="/register">
                  <Button size="lg">Começar Agora</Button>
                </Link>
                <Link href="/login" className="text-sm font-semibold leading-6 text-gray-900">
                  Já tenho conta <span aria-hidden="true">→</span>
                </Link>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
