import React from 'react';
import { Card, CardContent } from './ui/Card';

export function LeadCard({ title, value, subtitle }: { title: string, value: string | number, subtitle?: string }) {
  return (
    <Card>
      <CardContent className="p-6">
        <p className="text-sm font-medium text-gray-500 truncate">{title}</p>
        <p className="mt-2 text-3xl font-semibold text-gray-900">{value}</p>
        {subtitle && <p className="mt-2 text-sm text-gray-500">{subtitle}</p>}
      </CardContent>
    </Card>
  );
}
